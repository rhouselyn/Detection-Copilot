from openai import OpenAI
import config
from windows import image_process

api_keys = ["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"]  # 多个API密钥
dialog = config.prompt


def generate_response(prompt):
    attempts = 0
    max_attempts = len(api_keys) * 2  # 最大尝试次数等于密钥数量
    error = ''

    while attempts < max_attempts:
        api_key = api_keys[attempts % len(api_keys)]  # 循环使用API密钥
        try:
            client = OpenAI(
                api_key=api_key,
            )

            response = client.chat.completions.create(
                messages=prompt,
                model="gpt-3.5-turbo-1106",
            )
            return response.choices[0].message.content

        except Exception as e:
            error = f"遇到错误使用API密钥：{api_key}，错误信息：{e}"
            print(error)
            attempts += 1
            continue

    return error

    # while attempts < max_attempts:
    #     api_key = api_keys[attempts % len(api_keys)]  # 循环使用API密钥
    #     try:
    #         client = OpenAI(
    #             api_key=api_key,
    #         )
    #
    #         response = client.chat.completions.create(
    #             messages=prompt,
    #             model="gpt-3.5-turbo-1106",
    #             stream=True,
    #         )
    #         return response
    #
    #     except Exception as e:
    #         print(e)
    #         attempts += 1
    #         continue
    # raise Exception("暂时无法调用api")


def clear_dialog():
    global dialog
    dialog = config.prompt


def get_output(prompt):
    global dialog
    max_length = 3000  # 最大字数限制

    threshold = config.threshold
    unique_labels = set()  # 创建一个空集合用于存储独特的标签
    for obj in image_process.current_total_objects:
        if obj['score'] < threshold:
            continue
        unique_labels.add(obj["label"])  # 添加标签到集合中

    current_total_objects = list(unique_labels)  # 将集合转换为列表

    prompt = f"""
total result: {current_total_objects}
model = {config.model}
threshold = {config.threshold}
label_color = {config.label_color}
box_color = {config.box_color}
is_label = {config.is_label}
is_score = {config.is_score}  

{prompt}
"""
    print(prompt)

    dialog.append({"role": "user", "content": prompt})
    output = generate_response(dialog)

    dialog.append({"role": "assistant", "content": output})

    if len(str(dialog)) > max_length:
        dialog.pop(2)
        dialog.pop(2)

    # Split the output into lines
    lines = output.split('\n')

    # Initialize variables
    code_lines = []
    reply_lines = []
    inside_code_block = False

    for line in lines:
        if '```' in line:
            inside_code_block = not inside_code_block
            continue
        if inside_code_block:
            code_lines.append(line)
        else:
            reply_lines.append(line)

    # Join lines to form the final code and reply strings
    code = '\n'.join(code_lines).strip()
    reply = '\n'.join(reply_lines).strip()

    print('code: ' + code if code else 'code: None')
    print('reply: ' + reply)

    return code, reply


def main():
    dialog = config.prompt
    max_length = 3000  # 最大字数限制

    while True:
        user_input = input("你：")
        dialog.append({"role": "user", "content": user_input})
        bot_response = generate_response(dialog)
        reply = ''
        print("GPT：")
        for part in bot_response:
            reply += part.choices[0].delta.content or ""
            print(part.choices[0].delta.content or "", end="")

        dialog.append({"role": "assistant", "content": reply})

        if len(str(dialog)) > max_length:
            dialog.pop(1)
            dialog.pop(1)


if __name__ == "__main__":
    main()
