import argparse
from src.utils import crawling_data

def args_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument("--news",
                        type=str,
                        default="bao_thanh_nien",
                        help="""Choose one of the options in ['bao_thanh_nien','bao_tuoi_tre','vnexpress'] to collect data""")

    parser.add_argument("--topic",
                        type=str,
                        default="",
                        help="""Parse kafka topic""")
    
    return parser.parse_args()

def main(args):
    crawling_data(args)


if __name__=='__main__':
    args=args_parser()
    main(args)