import config


def run_code(code_fragment):
    if not code_fragment:
        return

    if "config.recover()" in code_fragment:
        config.recover()
        # 去除这一行
        code_fragment = code_fragment.replace("config.recover()\n", "")

    code = f"""  
import config

model = config.model
object_list = config.object_list
threshold = config.threshold
label_color = config.label_color
box_color = config.box_color
is_label = config.is_label
is_score = config.is_score

{code_fragment}

config.model = model
config.object_list = object_list
config.threshold = threshold
config.label_color = label_color
config.box_color = box_color
config.is_label = is_label
config.is_score = is_score

    """
    try:
        exec(code)
    except Exception as e:
        print(e)
