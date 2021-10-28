import logging


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO,
    )
    logger = logging.getLogger('bot_logger')


if __name__ == '__main__':
    main()