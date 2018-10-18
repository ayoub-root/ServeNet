import pandas
import numpy as np
import os
import matplotlib.pyplot as plt
import json

basic_path = 'D:\python_projects\ServeNet_others'

top5_json_files = []
if os.path.exists(basic_path):
    files = os.listdir(basic_path)
    for f in files:
        if 'top1_' in f:
            top5_json_files.append(f)

print('Top5 files num: ', len(top5_json_files), top5_json_files)

# generate
method_names = ["AdaBoost","Attention-LSTM","BI-LSTM","C-LSTM","CNN","LDA-Linear-SVM","LDA-RBF-SVM","LSTM","NaiveBayes",
                "RF","Recurrent-CNN","ServeNet"]
print(len(top5_json_files) == len(method_names))

categories = ["Tools","Financial","Messaging","eCommerce","Payments","Social","Enterprise","Mapping","Telephony","Science",
          "Government","Email","Security","Reference","Video","Travel","Sports","Search","Advertising","Transportation",
          "Education","Games","Music","Photos","Cloud","Bitcoin","Project Management","Data","Backend","Database",
          "Shipping","Weather","Application Development","Analytics","Internet of Things","Medical","Real Estate",
          "Events","Banking","Stocks","Entertainment","Storage","Marketing","File Sharing","News Services","Domains",
          "Chat","Media","Images","Other"]

ordered_method_names = ["CNN", "AdaBoost", "LDA-Linear-SVM", "LDA-RBF-SVM", "NaiveBayes", "LSTM", "RF", "Recurrent-CNN",
                        "C-LSTM", "Attention-LSTM", "BI-LSTM", "ServeNet"]
columns = ["Method", "Tools","Financial","Messaging","eCommerce","Payments","Social","Enterprise",
                               "Mapping","Telephony","Science",
          "Government","Email","Security","Reference","Video","Travel","Sports","Search","Advertising","Transportation",
          "Education","Games","Music","Photos","Cloud","Bitcoin","Project Management","Data","Backend","Database",
          "Shipping","Weather","Application Development","Analytics","Internet of Things","Medical","Real Estate",
          "Events","Banking","Stocks","Entertainment","Storage","Marketing","File Sharing","News Services","Domains",
          "Chat","Media","Images","Other"]

df = pandas.DataFrame(columns=columns)

for i in range(len(ordered_method_names)):
    method = ordered_method_names[i]
    file_index = method_names.index(method)
    file_name = top5_json_files[file_index]
    print('file name:', file_name)

    ab_path = os.path.join(basic_path, file_name)

    with open(ab_path, 'r') as f:
        array = json.load(f)
        data = [method]
        for cate in categories:
            value = array[cate]
            data.append(value)
        df.loc[i] = data

    print("finish add rows")

print(df)

df.to_csv('df.csv', index=False)

# draw radar figure
labels = categories
kinds = list(df.iloc[:, 0])
print(labels, kinds)

df = pandas.concat([df, df[[labels[0]]]], axis=1)
centers = np.array(df.iloc[:, 1:])

n = len(labels)
angle = np.linspace(0, 2 * np.pi, endpoint=False)
angle = np.concatenate((angle, [angle[0]]))

fig = plt.figure(figsize=(500, 500))

ax = fig.add_subplot(111, polar=True)    # 参数polar, 以极坐标的形式绘制图形

# 画线
for i in range(len(kinds)):

    if i == len(kinds) - 1:
        ax.plot(angle, centers[i], linewidth=3, color='red', label=kinds[i])
    else:
        ax.plot(angle, centers[i], linewidth=1, label=kinds[i])
    # ax.fill(angle, centers[i])  # 填充底色

# 添加属性标签
ax.set_thetagrids(angle * 180 / np.pi, labels)
plt.title('Categories')
plt.legend(loc='lower left', bbox_to_anchor=(1, 0.7))
plt.show()
