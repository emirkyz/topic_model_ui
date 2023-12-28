import time

import numpy as np
import pandas as pd
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer


class NMF_model():
    def __init__(self):
        super().__init__()

        self.model = NMF(n_components=10, init='nndsvd')
        self.vectorizer = TfidfVectorizer(min_df=50, stop_words='english')

    def NMF_func(self, win, df, qApp, num_topics):
        qApp.processEvents()
        win.plainTextEdit.setPlainText(win.plainTextEdit.toPlainText() + "\n" + "Veriler Yükleniyor (1/6)\n")
        win.plainTextEdit.setPlainText(
            win.plainTextEdit.toPlainText() + "\n" + f"Seçilen Konu Sayısı: {num_topics}")
        documents = df

        # print(documents.head())
        # print(documents.shape)

        qApp.processEvents()
        win.plainTextEdit.setPlainText(
            win.plainTextEdit.toPlainText() + "\n" + "Dökümanlar Vektörleştiriliyor, Durak Kelimeler Çıkartılıyor. (2/6)\n")

        # self.vectorizer = TfidfVectorizer(min_df=50, stop_words='english')

        X = self.vectorizer.fit_transform(documents.headline_text)
        df_features = self.vectorizer.get_feature_names_out()
        df_features = pd.DataFrame(df_features)
        # df_features.to_csv('df_features.csv')

        # list = [5790, 1468, 2224, 2752, 215]
        # for name, age in vect.vocabulary_.items():
        #     if age in list:
        #         print(name, age)
        # print(X[0, :])

        genel_toplam_eleman_sayisi = X.shape[0] * X.shape[1]
        qApp.processEvents()
        win.plainTextEdit.setPlainText(
            win.plainTextEdit.toPlainText() + "\n" + f"Matrisde bulunan toplam eleman sayısı: {genel_toplam_eleman_sayisi}")
        win.plainTextEdit.moveCursor(win.plainTextEdit.textCursor().End)
        # print("Saving the small portion of vectorized documents\n")
        # print("Matrisden rasgele 1000 eleman seçiliyor\n")
        smaller_x = X[np.random.choice(X.shape[0], 1000, replace=False)]
        #
        x_df = np.array(smaller_x.todense())
        # print(f"Matrisin boyutu: {x_df.shape}")
        # print(f"Matrisde bulunan toplam eleman sayısı: {x_df.size}")
        # zero_count = np.count_nonzero(x_df == 0)
        # print(f"Matrisde bulunan toplam 0 sayısı: {np.count_nonzero(x_df == 0)}")
        # print(f"Matrisin bosluk oranı: %{(zero_count / x_df.size) * 100}")
        # print("-------------------------------")
        x_df = pd.DataFrame(x_df)
        # x_df.to_csv('x_df.csv')
        # Create an NMF instance: model
        # the 10 components will be the topics

        # seminer_3
        qApp.processEvents()
        win.plainTextEdit.setPlainText(win.plainTextEdit.toPlainText() + "\n" + "NMF Modeli Çalıştırılıyor. (3/6)\n")

        self.model = NMF(n_components=num_topics, init='nndsvd')

        self.model.fit(X)

        nmf_features = self.model.transform(X)

        qApp.processEvents()
        win.plainTextEdit.setPlainText(
            win.plainTextEdit.toPlainText() + "\n" + "Çıktılar Kaydediliyor. (4/6)\n")
        # Create a DataFrame: components_df

        components_df = pd.DataFrame(self.model.components_, columns=self.vectorizer.get_feature_names_out())
        # components_df.to_csv('components_df.csv')

        W = self.model.fit_transform(X)
        w_df = pd.DataFrame(W)
        # w_df.to_csv('w_df.csv')

        H = self.model.components_
        h_df = pd.DataFrame(H)

        # h_df.to_csv('h_df.csv')

        win.plainTextEdit.setPlainText(win.plainTextEdit.toPlainText() + "\n" + f"X'in Boyutu : {X.shape}")

        win.plainTextEdit.setPlainText(
            win.plainTextEdit.toPlainText() + "\n" + f"W'nin Boyutu : {W.shape} ve H'ın Boyutu : {H.shape}")
        win.plainTextEdit.moveCursor(win.plainTextEdit.textCursor().End)

        # print(components_df.head())
        win.plainTextEdit.setPlainText(
            win.plainTextEdit.toPlainText() + "\n" + "Her Konu İçin En Yüksek Değere Sahip Kelimeler Elde Ediliyor. (5/6)\n")
        win.plainTextEdit.moveCursor(win.plainTextEdit.textCursor().End)
        qApp.processEvents()
        for topic in range(components_df.shape[0]):
            tmp = components_df.iloc[topic]
            win.plainTextEdit.setPlainText(
                win.plainTextEdit.toPlainText() + "\n" + f' {topic + 1}. Konu için En Yüksek Değere Sahip Kelimeler :')
            win.plainTextEdit.setPlainText(
                win.plainTextEdit.toPlainText() + "\n" + f'{tmp.nlargest(10)}' + "\n")
            win.plainTextEdit.moveCursor(win.plainTextEdit.textCursor().End)
            qApp.processEvents()
            time.sleep(2)

        win.plainTextEdit.moveCursor(win.plainTextEdit.textCursor().End)
        feat_names = self.vectorizer.get_feature_names_out()

        qApp.processEvents()

        word_dict = {}
        for i in range(num_topics):
            # for each topic, obtain the largest values, and add the words they map to into the dictionary.
            words_ids = self.model.components_[i].argsort()[:-10 - 1:-1]
            words = [feat_names[key] for key in words_ids]
            word_dict['Topic # ' + '{:02d}'.format(i + 1)] = words
        result = pd.DataFrame(word_dict)

        my_document = documents.headline_text[72]
        win.plainTextEdit.setPlainText(
            win.plainTextEdit.toPlainText() + "\n" + "72.ci Dökümanın En Yüksek Değere Sahip Konusu Getiriliyor (6/6)\n")
        qApp.processEvents()
        win.plainTextEdit.setPlainText(win.plainTextEdit.toPlainText() + "\n" + f"{my_document}")
        win.plainTextEdit.setPlainText(
            win.plainTextEdit.toPlainText() + "\n" + f"{pd.DataFrame(nmf_features).loc[72]}")
        win.plainTextEdit.moveCursor(win.plainTextEdit.textCursor().End)

        # print(my_document)
        # print(pd.DataFrame(nmf_features).loc[55])
        nmf_features_df = pd.DataFrame(nmf_features)
        # nmf_features_df.to_csv('nmf_features_df.csv')

        w_df.columns += 1
        w_df['topic_id'] = w_df.idxmax(axis=1)
        h_df.columns += 1
        return x_df, w_df, h_df, result

    def tahmin_et(self, metin):
        my_news = f"""{metin}"""

        X_tahmin = self.vectorizer.transform([my_news])
        nmf_features = self.model.transform(X_tahmin)
        x_nmf_transformed = pd.DataFrame(nmf_features)
        sonuclar = pd.DataFrame(nmf_features)
        sonuclar.columns += 1

        return sonuclar

# --------------------------------------------


# print("Making new prediction")
# my_news = """Police investigating the shooting near the intersection of 3rd Avenue and Pine Street"""
#
# # my_news = """15-year-old girl stabbed to death in grocery store during fight with 4 younger girls
# #         Authorities said they gathered lots of evidence from videos on social media"""
# num_topics = 10
# # Transform the TF-IDF
# X = vect.transform([my_news])
# x_vec_transformed = pd.DataFrame(X)
# x_vec_transformed.to_csv('x_vec_transformed.csv')
# # Transform the TF-IDF: nmf_features
# nmf_features = model.transform(X)
#
# x_nmf_transformed = pd.DataFrame(nmf_features)
# x_nmf_transformed.to_csv('x_nmf_transformed.csv')
#
# sonuclar = pd.DataFrame(nmf_features)
# print(pd.DataFrame(nmf_features).idxmax(axis=1))
# print("Done")
# # print(pd.DataFrame(nmf_features).idxmax(axis=1).value_counts())
