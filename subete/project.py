import logging

logger = logging.getLogger(__name__)

class Project:
    """
    An object representing a Project in the Sample Programs repo.

    :param name: the name of the project in its pathlike form (e.g., hello-world) 
    """

    def __init__(self, name: str):
        self._name: str = name
        self._requirements_url: str = self._generate_requirements_url()

    def __str__(self) -> str:
        return self.name()

    def name(self) -> str:
        """
        Retrieves the name of the project in its human-readable form.

        Assuming you have a Project object called project, here's how you would
        use this method::

            name: str = project.name()

        :return: the name of the project as a string
        """
        _project_name = (
            self._name.replace("-", " ").title() 
            if len(self._name) <= 3 
            else self._name.upper()
        )
        return _project_name

    def pathlike_name(self) -> str:
        """
        Retrieves the name of the project in its pathlike form (e.g., hello-world).

        Assuming you have a Project object called project, here's how you would
        use this method::

            pathlike_name: str = project.pathlike_name()

        :return: the name of the project in its pathlike form as a string
        """
        return self._name

    def requirements_url(self) -> str:
        """
        Retrieves the URL to the requirements documentation for
        this sample program. Requirements URL is assumed to exist
        and therefore not validated. The requirements documentation 
        URL is in the following form:

        ``https://sampleprograms.io/projects/{project}/``

        For example, here is a link to the
        `Hello World documentation <https://sampleprograms.io/projects/hello-world/>`_. 

        Assuming you have a SampleProgram object called program, 
        here's how you would use this method::

            url: str = program.requirements_url()

        :return: the requirments URL as a string 
        """
        logger.info(f'Retrieving requirements URL for {self}: {self._sample_program_req_url}')
        return self._sample_program_req_url

    def _generate_requirements_url(self) -> str:
        """
        A helper method for generating the expected requirements URL 
        for this sample program.

        :return: the expected requirements URL 
        """
        doc_url_base = "https://sampleprograms.io/projects"
        if "export" in self.pathlike_name() or "import" in self.pathlike_name():
            return f"{doc_url_base}/import-export"
        else:
            return f"{doc_url_base}/{self.pathlike_name()}"
