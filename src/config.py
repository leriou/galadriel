import configparser


class ConfigParser:

    def getContent(self, filename):
        parser = configparser.ConfigParser()
        parser.read(filename)
        return parser


if __name__ == '__main__':
    cf = ConfigParser()
    hd = cf.getContent("config.ini")
    print(hd.get("redis", "host"))
