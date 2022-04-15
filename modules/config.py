import json
import os
import cv2 as cv

from modules.uitils import Utils
script_dir = os.path.dirname(__file__)
img_dir = os.path.join(os.path.abspath(
    os.path.dirname(script_dir+os.path.sep+'.')), 'imgs/')

print(img_dir)


class Item(Utils):
    def __init__(self, hwnd, item_config, global_data) -> None:
        # 默认cv.TM_SQDIFF_NORMED 效果最好
        if item_config.match is not None and item_config.match.method is not None:
            match_template_method = cv[item_config.match.method]
        else:
            match_template_method = cv.TM_SQDIFF_NORMED
        super().__init__(hwnd, match_template_method)
        self.config = item_config
        self.global_data = global_data

    def run(self):
        try:
            flag = True
            index = 0
            while index < 3 and flag is True:
                if index == 0:
                    if self.confg.judge is not None and self.confg.judge.time == 'before':
                        flag = self.judge()
                elif index == 1:
                    flag = self.match_img()
                else:
                    if self.confg.judge is not None and self.confg.judge.time == 'after':
                        flag = self.judge()
                index = index + 1
            else:
                self.reject()
            if flag is True:
                self.resolve()

        except BaseException as err:
            print(f"Unexpected {err=}, {type(err)=}")

    def judge(self):
        values = [self.global_data[x]
                  for x in self.config.judge.getProperty]
        flag = None
        if self.config.judge.relation == 'and':
            flag = True
            for i in len(values):
                operator = self.config.judge.operator[i]
                match operator:
                    case '>':
                        flag = flag and values[i] > self.config.judge.judgeValue[i]

                    case '<':
                        flag = flag and values[i] < self.config.judge.judgeValue[i]

                    case '>=':
                        flag = flag and values[i] >= self.config.judge.judgeValue[i]

                    case '<=':
                        flag = flag and values[i] <= self.config.judge.judgeValue[i]

                    case '=':
                        flag = flag and values[i] == self.config.judge.judgeValue[i]

                    case 'is':
                        flag = flag and values[i] is self.config.judge.judgeValue[i]

                    case 'in':
                        flag = flag and values[i] in self.config.judge.judgeValue[i]

                    case _:
                        flag = False
                if flag is False:
                    break
        elif self.config.judge.relation == 'or':
            flag = False
            for i in len(values):
                operator = self.config.judge.operator[i]
                match operator:
                    case '>':
                        flag = flag or values[i] > self.config.judge.judgeValue[i]

                    case '<':
                        flag = flag or values[i] < self.config.judge.judgeValue[i]

                    case '>=':
                        flag = flag or values[i] >= self.config.judge.judgeValue[i]

                    case '<=':
                        flag = flag or values[i] <= self.config.judge.judgeValue[i]

                    case '=':
                        flag = flag or values[i] == self.config.judge.judgeValue[i]

                    case 'is':
                        flag = flag or values[i] is self.config.judge.judgeValue[i]

                    case 'in':
                        flag = flag or values[i] in self.config.judge.judgeValue[i]

                    case _:
                        flag = False
                if flag is True:
                    break
        return flag

    def match_img(self):
        source = self.background_screenshot(self.hwnd)
        sample_url = os.path.join(img_dir, self.config.match.sample)
        sample = cv.imread(sample_url)
        result = self.template_matching(sample, source)
        if result is not None:
            self.position = result
            return True
        else:
            return False

    def reject(self):
        pass

    def resolve(self):
        pass


class Config:
    def __init__(self, rel_path) -> None:
        super(Config, self).__init__()
        abs_path = os.path.join(script_dir, rel_path)
        with open(abs_path) as f:
            self.dictionary = json.load(f)
            print('typeof dictionary', type(self.dictionary), self.dictionary)

    def getFirstItem(self):
        return list(self.dictionary.values())[0]

    def getItem(self, tag):
        return self.dictionary[tag]
