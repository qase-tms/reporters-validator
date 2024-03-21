import argparse


class Config:
    def __init__(self, mode, project_code, token, output, testrun_id, input):
        self.input = input
        self.mode = mode
        self.project_code = project_code
        self.token = token
        self.output = output
        self.testrun_id = testrun_id


class ConfigManager:
    def __init__(self):
        self.__parser = argparse.ArgumentParser()
        self.__add_arguments()
        self.__parse_arguments()
        self.__validate_config()

    def __add_arguments(self):
        self.__parser.add_argument('-m', '--mode', default="validate", type=str,
                                   help='Mode of operation: prepare or validate')

        self.__parser.add_argument('-pc', '--project-code', type=str,
                                   help='Code of Qase project', required=True)

        self.__parser.add_argument('-t', '--token', type=str,
                                   help='Token for Qase API', required=True)

        self.__parser.add_argument('-ti', '--testrun-id', type=str,
                                   help='Test run id for Qase API', required=True)

        self.__parser.add_argument('-o', '--output', type=str,
                                   help='Output file for results')

        self.__parser.add_argument('-i', '--input', type=str,
                                   help='Input file for results')

    def __parse_arguments(self):
        args = self.__parser.parse_args()
        self.__config = Config(args.mode, args.project_code.upper(), args.token, args.output, args.testrun_id,
                               args.input)

    def __validate_config(self):
        if self.__config.mode not in ["prepare", "validate"]:
            raise ValueError("Mode must be either 'prepare' or 'validate'")

        if self.__config.mode == "prepare":
            if not self.__config.output:
                raise ValueError("Output file is required then mode is 'prepare'")
        else:
            if not self.__config.input:
                raise ValueError("Input file is required then mode is 'validate'")

    def get_config(self) -> Config:
        return self.__config
