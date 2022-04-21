import json
import os
import random
import time
import cv2 as cv

from modules.uitils import Utils
script_dir = os.path.dirname(__file__)
img_dir = os.path.join(script_dir, '../imgs/')
config_dir = os.path.join(script_dir, '../config/')


class Item(Utils):
    def __init__(self, hwnd, item_config, global_data, tag, filename, screen) -> None:
        # 默认cv.TM_SQDIFF_NORMED 效果最好
        if 'match' in item_config and item_config['match'] is not None and item_config['match']['method'] is not None:
            match_template_method = eval(
                'cv.' + item_config['match']['method'])
        else:
            match_template_method = cv.TM_SQDIFF_NORMED
        super().__init__(hwnd, match_template_method, tag, filename, screen)
        self.config = item_config
        self.global_data = global_data
        self.run_num = 0
        self.next = None
        if 'next' in item_config:
            self.next = item_config['next']
        if 'debug' in item_config:
            self.debug = item_config['debug']

    def run(self):
        self.run_num = self.run_num + 1
        try:
            flag = True
            index = 0
            while index < 3 and flag is True:
                if index == 0:
                    if "judge" in self.config and self.config["judge"] is not None and self.config["judge"]["time"] == 'before':
                        flag = self.judge()
                elif index == 1:
                    flag = self.match_img()
                else:
                    if "judge" in self.config and self.config["judge"] is not None and self.config["judge"]["time"] == 'after':
                        flag = self.judge()
                index = index + 1

            if flag is True:
                self.resolve()
            else:
                self.reject()

        except BaseException as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise

    def judge(self):
        judge = self.config['judge']
        if "getProperty" in judge and 'operator' in judge and 'relation' in judge:
            values = [self.global_data[x]
                      for x in judge["getProperty"]]
            flag = None
            if judge["relation"] == 'and':
                flag = True
                for i in range(len(values)):
                    operator = judge["operator"][i]
                    match operator:
                        case '>':
                            flag = flag and values[i] > judge["judgeValue"][i]

                        case '<':
                            flag = flag and values[i] < judge["judgeValue"][i]

                        case '>=':
                            flag = flag and values[i] >= judge["judgeValue"][i]

                        case '<=':
                            flag = flag and values[i] <= judge["judgeValue"][i]

                        case '=':
                            flag = flag and values[i] == judge["judgeValue"][i]

                        case 'is':
                            flag = flag and values[i] is judge["judgeValue"][i]

                        case 'in':
                            flag = flag and values[i] in judge["judgeValue"][i]

                        case _:
                            flag = False
                    if flag is False:
                        break
            elif judge["relation"] == 'or':
                flag = False
                for i in range(len(values)):
                    operator = judge["operator"][i]
                    match operator:
                        case '>':
                            flag = flag or values[i] > judge["judgeValue"][i]

                        case '<':
                            flag = flag or values[i] < judge["judgeValue"][i]

                        case '>=':
                            flag = flag or values[i] >= judge["judgeValue"][i]

                        case '<=':
                            flag = flag or values[i] <= judge["judgeValue"][i]

                        case '=':
                            flag = flag or values[i] == judge["judgeValue"][i]

                        case 'is':
                            flag = flag or values[i] is judge["judgeValue"][i]

                        case 'in':
                            flag = flag or values[i] in judge["judgeValue"][i]

                        case _:
                            flag = False
                    if flag is True:
                        break
            return flag
        print('配置错误，请输入 getProperty、operator、relation')
        return False

    def match_img(self):
        if 'match' in self.config and 'sample' in self.config['match'] and self.config["match"]["sample"] is not None:
            source = self.background_screenshot(self.hwnd)
            sample_url = os.path.join(img_dir, self.config["match"]["sample"])
            sample = cv.imread(sample_url)
            rate = 0.1 if self.match_template_method in [
                cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED] else 0.8
            if 'rete' in self.config["match"]:
                rate = float(self.config["match"]['rate'])
            if 'targetNum' in self.config['match']:
                targetNum = self.config["match"]['targetNum']
            result = self.template_matching(sample, source, rate, targetNum)
            if "saveAs" in self.config["match"]:
                self.global_data[self.config["match"]["saveAs"]
                                 ] = True if result is not None else False
            if result is not None:
                self.position = result
                return True
            else:
                return False
        return True

    def reject(self):
        if 'reject' in self.config and self.config["reject"] is not None:
            reject = self.config["reject"]
            if 'sleepRandom' in reject and isinstance(reject['sleepRandom'], float):
                time.sleep(random.random(0, reject['sleepRandom']))
            if 'sleep' in reject and isinstance(reject['sleep'], int):
                time.sleep(reject['sleep'])
            if "retry" in reject and reject["retry"] is not None and self.run_num < reject["retry"]:
                self.run()
            elif 'jump' in reject and reject["jump"] is not None:
                self.next = reject["jump"]

    def resolve(self):
        resolve = None
        if 'resolve' in self.config:
            resolve = self.config["resolve"]
        if resolve is not None:
            if 'setProperty' in resolve and isinstance(resolve["setProperty"], list) and "propertyValue" in resolve is not None and isinstance(resolve["propertyValue"], list) and len(resolve["propertyValue"]) == len(resolve["setProperty"]):
                for i in range(len(resolve["setProperty"])):
                    match resolve["propertyValue"][i]:
                        case 'sum':
                            if resolve["setProperty"][i] not in self.global_data or self.global_data[resolve["setProperty"][i]] is None:
                                self.global_data[resolve["setProperty"][i]] = 0
                            self.global_data[resolve["setProperty"][i]
                                             ] = self.global_data[resolve["setProperty"][i]] + 1
                        case  "sub":
                            if resolve["setProperty"][i] not in self.global_data or self.global_data[resolve["setProperty"][i]] is None:
                                self.global_data[resolve["setProperty"][i]] = 0
                            self.global_data[resolve["setProperty"][i]
                                             ] = self.global_data[resolve["setProperty"][i]] - 1
                        case _:
                            self.global_data[resolve["setProperty"][i]
                                             ] = resolve["propertyValue"][i]
            if 'do' in resolve:
                if resolve["do"] == 'click':
                    self.click()
                elif resolve["do"] == 'jump':
                    self.next = resolve["jump"]

    def click(self):
        if 'click' in self.config:
            click = self.config["click"]
            if self.position is not None and click is not None:
                left_top, right_bottom = self.position
                x1, y1 = left_top
                x2, y2 = right_bottom
                base = (x1+int((x2 - x1)/2), y1+int((y2-y1)/2))
                if "positionBase" in click:
                    match click["positionBase"]:
                        case 'leftTop':
                            base = left_top
                        case 'rightTop':
                            base = (x2, y1)
                        case 'leftBottom':
                            base = (x1, y2)
                        case 'rightBottom':
                            base = right_bottom
                        case 'center':
                            base = (x1+int((x2 - x1)/2), y1+int((y2-y1)/2))
                if "offset" in click:
                    x, y = click["offset"]
                    x0, y0 = base
                    base = (x0+x, y0+y)
                if "random" in click and isinstance(click["random"], int):
                    randomx = random.randint(-click["random"], click["random"])
                    randomy = random.randint(-click["random"], click["random"])
                    x, y = base
                    base = (x+randomx, y+randomy)
                x, y = base
                self.do_click(self.hwnd, x, y)


class Config:
    def __init__(self, rel_path) -> None:
        super(Config, self).__init__()
        abs_path = os.path.join(config_dir, rel_path)
        with open(abs_path) as f:
            self.dictionary = json.load(f)

    def getFirstItem(self):
        return list(self.dictionary.values())[0]

    def getItem(self, tag):
        return self.dictionary[tag]
