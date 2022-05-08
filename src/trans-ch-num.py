import json
import sys

print(sys.argv)

with open(sys.argv[2], "w") as output:
    with open(sys.argv[1]) as intput:
        for line in intput:
            data = json.loads(line)
            titles = data["title"].split(sys.argv[3])
            titles[0] = (
                titles[0]
                .replace("一", "1")
                .replace("二", "2")
                .replace("廿", "2")
                .replace("甘", "2")
                .replace("三", "3")
                .replace("卅", "3")
                .replace("四", "4")
                .replace("五", "5")
                .replace("六", "6")
                .replace("七", "7")
                .replace("八", "8")
                .replace("九", "9")
                .replace("零", "0")
            )
            if titles[0].startswith("第百十"):
                titles[0] = titles[0].replace("百十", "11")
            if titles[0].startswith("第百"):
                titles[0] = titles[0].replace("百", "1")
            if titles[0].startswith("第十"):
                titles[0] = titles[0].replace("十", "1")
                if titles[0] == "第1":
                    titles[0] = titles[0] + "0"
            if titles[0].endswith("十"):
                titles[0] = titles[0].replace("十", "0")
            if titles[0].endswith("百"):
                titles[0] = titles[0].replace("百", "00")
            if titles[0].endswith("千"):
                titles[0] = titles[0].replace("千", "000")
            titles[0] = titles[0].replace("百", "").replace("十", "").replace("千", "")
            data["title"] = sys.argv[3].join(titles)
            output.write(json.dumps(data, ensure_ascii=False) + "\n")
