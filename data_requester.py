from common_imports import *
from constants import *
from aiohttp import ClientSession
from tenacity import retry, wait_fixed, stop_after_attempt


@retry(wait=wait_fixed(1), stop=stop_after_attempt(3))
async def make_request(url: str, 
                       semaphore: asyncio.Semaphore, 
                       session: ClientSession) -> dict:
    """
    Make a GET request to the specified URL.

    Args:
        url (str): The URL to send the GET request to.
        semaphore (asyncio.Semaphore): The semaphore to limit the number of concurrent requests.
        session (aiohttp.ClientSession): The session to use for making the request.

    Returns:
        dict: The JSON response from the server.
    """
    async with semaphore:
        async with session.get(url) as response:
            return await response.json()


async def get_data_by_ids(url: str, 
                          ids: list, 
                          session: ClientSession, 
                          semaphore: asyncio.Semaphore, 
                          foreign_id_column_name: str = None) -> pd.DataFrame:
    """
    Get data from the specified URL for each ID in the list of IDs.

    Args:
        url (str): The base URL to send the GET request to.
        ids (list): The list of IDs to append to the URL.
        session (aiohttp.ClientSession): The session to use for making the request.
        semaphore (asyncio.Semaphore): The semaphore to limit the number of concurrent requests.
        foreign_id_column_name (str, optional): The name of the column to add to the DataFrame that will contain the ID used in the request. Defaults to None.

    Returns:
        pd.DataFrame: A DataFrame containing the data returned from the server for each ID.
    """
    tasks = [asyncio.create_task(
        make_request(url + str(id), semaphore, session)
    ) for id in ids]
    results = await asyncio.gather(*tasks)
    data_frames = pd.DataFrame()
    for result, id in zip(results, ids):
        data_frame_by_id = pd.DataFrame.from_dict(result)
        if foreign_id_column_name:
            data_frame_by_id[foreign_id_column_name] = id
        data_frames = pd.concat([data_frames, data_frame_by_id], ignore_index=True)
    return data_frames.drop_duplicates()


async def get_data_params(years: list) -> pd.DataFrame:
    """
    Get data parameters for the specified years.

    Args:
        years (list): The list of years to get data parameters for.

    Returns:
        pd.DataFrame: A DataFrame containing the data parameters for each year.
    """
    async with ClientSession() as session:
        semaphore = asyncio.Semaphore(100)
        journals = await get_data_by_ids(JOURNALS_BY_YEAR_REQUEST_URL, years, session, semaphore)
        params = journals.filter(["Year", "DirectionName", "Speciality"])
    return params.drop_duplicates()


async def get_univeris_data(years: list, 
                            qualifications: list, 
                            direction_names: list) -> tuple:
    """
    Get university data for the specified years, qualifications, and direction names.

    Args:
        years (list): The list of years to get data for.
        qualifications (list): The list of qualifications to get data for.
        direction_names (list): The list of direction names to get data for.

    Returns:
        tuple: A tuple containing DataFrames for journals, students, grades, ratings, and EGE.
    """
    def to_list_if_not(obj):  # Returns the list if the object is not sequence
        if isinstance(obj, list):
            return obj
        return [obj]
        
    years = to_list_if_not(years)
    qualifications = to_list_if_not(qualifications)
    direction_names = to_list_if_not(direction_names)
        
    async with ClientSession() as session:
        semaphore = asyncio.Semaphore(100)
        
        # getting journals 
        journals = await get_data_by_ids(JOURNALS_BY_YEAR_REQUEST_URL, 
                                         years, 
                                         session, 
                                         semaphore)
        if direction_names:
            journals = journals[
                journals["DirectionName"].isin(direction_names)]
        if qualifications:
            journals = journals[
                journals["Speciality"].isin(qualifications)]
            
        journal_ids = journals['Id'].unique()

        # getting students
        students = await get_data_by_ids(STUDENTS_BY_JOURNAL_REQUEST_URL, 
                                         journal_ids, 
                                         session, 
                                         semaphore, 
                                         "JournalId")
        students_ids = students["Id"].unique()

        # getting grades
        grades = await get_data_by_ids(GRADES_BY_JOURNAL_REQUEST_URL, 
                                       journal_ids, 
                                       session, 
                                       semaphore, 
                                       "JournalId")
    
        # getting ratings
        ratings = await get_data_by_ids(RATINGS_BY_JOURNAL_REQUEST_URL, 
                                        journal_ids, 
                                        session, 
                                        semaphore, 
                                        "JournalId")

        # getting ege
        ege = await get_data_by_ids(EGE_BY_STUDENT_REQUEST_URL, 
                                    students_ids, 
                                    session, 
                                    semaphore, 
                                    "StudentId")

    return journals, students, grades, ratings, ege