import sys, os

from splunklib.searchcommands import dispatch, StreamingCommand, Configuration, Option
from splunklib.searchcommands.validators import Fieldname
import pickle
import splunk
import logging, logging.handlers

from scripts.model import MarkovModel


def setup_logging():
    logger = logging.getLogger('splunk.anomark')
    SPLUNK_HOME = os.environ['SPLUNK_HOME']

    LOGGING_DEFAULT_CONFIG_FILE = os.path.join(SPLUNK_HOME, 'etc', 'log.cfg')
    LOGGING_LOCAL_CONFIG_FILE = os.path.join(SPLUNK_HOME, 'etc', 'log-local.cfg')
    LOGGING_STANZA_NAME = 'python'
    LOGGING_FILE_NAME = "anomark.log"
    BASE_LOG_PATH = os.path.join('var', 'log', 'splunk')
    LOGGING_FORMAT = "%(asctime)s %(levelname)-s\t%(module)s:%(lineno)d - %(message)s"
    splunk_log_handler = logging.handlers.RotatingFileHandler(
        os.path.join(SPLUNK_HOME, BASE_LOG_PATH, LOGGING_FILE_NAME), mode='a')
    splunk_log_handler.setFormatter(logging.Formatter(LOGGING_FORMAT))
    logger.addHandler(splunk_log_handler)
    splunk.setupSplunkLogger(logger, LOGGING_DEFAULT_CONFIG_FILE, LOGGING_LOCAL_CONFIG_FILE, LOGGING_STANZA_NAME)
    return logger


model_dump_field_dict = {
    "CommandLine": "model_cmdline.dump"
}


@Configuration()
class AnoMark(StreamingCommand):
    logger = setup_logging()

    fieldname = Option(doc='''
    **Syntax:** **fieldname=***<fieldname>*
    **Description:** Field on which to apply AnoMark computation

    ''', validate=Fieldname())

    modelname = Option(doc='''
    **Syntax:** **modelname=***<string>*
    **Description:** Name of the model to use, must be <AnoMark_APP>/bin/models

    ''')

    def stream(self, records):
        logger = self.logger
        fieldname = self.fieldname if self.fieldname else "CommandLine"
        modelname = self.modelname

        # choose the model to apply
        if modelname is None:
            try:
                modelname = model_dump_field_dict[fieldname]
            except KeyError:
                logger.error('no model found for field ' + fieldname)
                self.write_error("no model found for field {}".format(fieldname))
                exit(1)

        model_path = sys.path[0] + '/models/' + modelname

        try:
            with open(model_path, "rb") as f:
                model: MarkovModel = pickle.load(f)
        except FileNotFoundError as e:
            logger.error('{} : {}'.format(model_path, str(e)))
            self.write_error('{} : {}'.format(model_path, str(e)))
            exit(1)

        order = model.order
        for record in records:
            record["markov_score"] = model.log_likelihood(order * "~" + str(record[fieldname]) + order * "~")
            yield record


if __name__ == "__main__":
    dispatch(AnoMark, sys.argv, sys.stdin, sys.stdout, __name__)
