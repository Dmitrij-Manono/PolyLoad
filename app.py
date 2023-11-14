from helpers.custom_logger import CustomLogger



def main():
    logger = CustomLogger()
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")
    logger.alert("alert message")
    logger.user("user message")


if __name__ == "__main__":
    main()