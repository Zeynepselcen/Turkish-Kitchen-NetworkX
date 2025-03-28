import json
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px
import geopandas as gpd
from collections import Counter



# JSON dosyasını yükleme
# file_path = "C:/Users/Lenovo/Desktop/SNA/Turkish-Kitchen-NetworkX/dataset.json" #
# file_path = "/Users/yusufkaya/Desktop/SNA-project/Turkish-Kitchen-NetworkX/dataset.json" , yusuf's pc directory
# file_path = "C:/Users/Lenovo/Desktop/SNA/Turkish-Kitchen-NetworkX/dataset.json"
file_path = "/Users/sekerismail/Desktop/Turkish-Kitchen-NetworkX/dataset.json" # ismail's path
with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

G = nx.Graph()

# Düğümleri ekleme
for yemek in data["nodes"]:
    G.add_node(
        yemek["id"],  # Düğüm kimliği
        name=yemek["name"],  # Yemek adı
        region=yemek["region"],  # Bölge
        category=yemek["category"],  # Kategori
        ingredients=yemek["ingredients"]  # Malzemeler
    )

# Kenarları oluşturma (ortak malzemelere göre bağlama)
for yemek1 in data["nodes"]:
    for yemek2 in data["nodes"]:
        if yemek1["id"] != yemek2["id"]:  # Aynı düğümü bağlamayın
            ortak_malzemeler = set(yemek1["ingredients"]) & set(yemek2["ingredients"])
            if ortak_malzemeler:  # Ortak malzeme varsa kenar oluştur
                G.add_edge(yemek1["id"], yemek2["id"], ortak_malzemeler=list(ortak_malzemeler))

# Graf bilgilerini yazdırma
print(f"Graf Düğüm Sayısı: {G.number_of_nodes()}")
print(f"Graf Kenar Sayısı: {G.number_of_edges()}")

# Düğümleri ve kenarları listeleme
print("Düğümler ve Özellikler:")
for node, data in G.nodes(data=True):
    print(f"{node}: {data}")

print("Kenarlar ve Özellikler:")
for edge in G.edges(data=True):
    print(edge)
    
# En fazla komşusu olan yemekleri bulma
degree_dict = dict(G.degree())  # Her düğümün derecesini (komşu sayısı) al
max_degree = max(degree_dict.values())  # Maksimum dereceyi bul

# En fazla komşusu olan düğümleri listeleme
most_connected_nodes = [node for node, degree in degree_dict.items() if degree == max_degree]

# En fazla komşusu olan 5 yemeği bulma
sorted_degree = sorted(degree_dict.items(), key=lambda x: x[1], reverse=True)
top_5_nodes = sorted_degree[:5]
                            

print(f"\nEn fazla komşusu olan yemekler: {G.nodes[max_degree]["name"]}")
for node in most_connected_nodes:
    print(f"Yemek ID: {node}, Yemek Adı: {G.nodes[node]['name']}, Komşu Sayısı: {max_degree}")

print(f"\nEn fazla komşusu olan 5 yemek:")
for node, degree in top_5_nodes:
    yemek = G.nodes[node]
    print(f"Yemek ID: {node}, Yemek Adı: {yemek['name']}, Komşu Sayısı: {degree}")

pos = nx.spring_layout(G, seed=42)

# kenar sayısını bulma
num_edges = G.number_of_edges()
print(f"Ağdaki kenar sayısı: {num_edges}")
# node sayısını bulma 
num_nodes = G.number_of_nodes()
print(f"Ağdaki düğüm sayısı: {num_nodes}")
# dereceler
degrees = [degree for _, degree in G.degree()]
plt.hist(degrees, bins=range(1, max(degrees) + 2), align='left', color='skyblue', edgecolor='black')
plt.title("Düğüm Dereceleri Dağılımı")
plt.xlabel("Komşu Sayısı (Derece)")
plt.ylabel("Düğüm Sayısı")
plt.show()

# Kümeleme Katsayısı (Clustering Coefficient)
clustering = nx.clustering(G)  # Her düğüm için kümeleme katsayısı
average_clustering = nx.average_clustering(G)  # Tüm grafın ortalama kümeleme katsayısı
print(f"Ortalama Kümeleme Katsayısı: {average_clustering}")

# En yüksek kümeleme katsayısına sahip 5 düğüm
top_clustering = sorted(clustering.items(), key=lambda x: x[1], reverse=True)[:5]
print("En yüksek kümeleme katsayısına sahip düğümler:")
for node, coef in top_clustering:
    print(f"Yemek ID: {node}, Adı: {G.nodes[node]['name']}, Kümeleme Katsayısı: {coef}")
# Bağlantı Bileşenleri (Connected Components)
components = list(nx.connected_components(G))
print(f"Graf, {len(components)} farklı bağlantılı bileşene sahiptir.")

# Her bileşenin düğümlerini yazdırma
for i, component in enumerate(components):
    print(f"Bileşen {i + 1}: {component}")
# Merkezilik Ölçümleri (Centrality Measures)
# Derece Merkeziliği (Degree Centrality)
degree_centrality = nx.degree_centrality(G)
top_degree = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
print("Derece merkeziliği en yüksek 5 düğüm:")
for node, centrality in top_degree:
    print(f"Yemek ID: {node}, Adı: {G.nodes[node]['name']}, Derece Merkeziliği: {centrality}")

# Betweenness Merkeziliği (Betweenness Centrality)
betweenness = nx.betweenness_centrality(G)
top_betweenness = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:5]
print("Betweenness merkeziliği en yüksek 5 düğüm:")
for node, centrality in top_betweenness:
    print(f"Yemek ID: {node}, Adı: {G.nodes[node]['name']}, Betweenness Merkeziliği: {centrality}")

# Shortest Path
#örnek
source = 1  # Kaynak düğüm ID'si
target = 36  # Hedef düğüm ID'si
if nx.has_path(G, source, target):
    path = nx.shortest_path(G, source=source, target=target)
    print(f"En kısa yol ({source} -> {target}): {path}")
else:
    print(f"{source} ve {target} arasında yol yok.")

# Çap (Diameter)
if nx.is_connected(G):
    diameter = nx.diameter(G)
    print(f"Grafın çapı (en uzun en kısa yol): {diameter}")
else:
    print("Graf bağlantılı değil, çap hesaplanamaz.")

# Topluluk Algılama (Community Detection)
# Girvan-Newman Algorithm
from networkx.algorithms.community import girvan_newman
import community as community_louvain

communities = next(girvan_newman(G))  # İlk topluluk bölünmesini al
for i, community in enumerate(communities):
    
    community_names = [G.nodes[node]["name"] for node in community]
    print(f"Topluluk {i + 1}: {sorted(community_names)}")


# Yoğunluk (Density)
density = nx.density(G)
print(f"Grafın yoğunluğu: {density}")
# Yemekler Arası Benzerlik Skoru
from networkx.algorithms.link_prediction import jaccard_coefficient
# Jaccard skorlarını hesaplama
jaccard_scores = []
for u, v, p in jaccard_coefficient(G, [(y1, y2) for y1 in G.nodes for y2 in G.nodes if y1 != y2]):
    yemek1_name = G.nodes[u]["name"]
    yemek2_name = G.nodes[v]["name"]
    jaccard_scores.append(p)
    
    print(f"Yemek {yemek1_name} ile Yemek {yemek2_name} arasındaki Jaccard Skoru: {p:.2f}")
plt.figure(figsize=(10, 6))
plt.hist(jaccard_scores, bins=10, color="lightblue", edgecolor="black")
plt.title("Yemekler Arasındaki Jaccard Skor Dağılımı", fontsize=16)
plt.xlabel("Jaccard Skoru", fontsize=14)
plt.ylabel("Yemek Çifti Sayısı", fontsize=14)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()

# Bölgelere göre yemek sayısı
# Hangi bölgelerin daha fazla çeşitliliğe sahip olduğunu gösterir.
regions = [G.nodes[n]["region"] for n in G.nodes]
region_counts = {region: regions.count(region) for region in set(regions)}

plt.figure(figsize=(10, 6))
plt.bar(region_counts.keys(), region_counts.values(), color="coral", edgecolor="black")
plt.title("Bölgelere Göre Yemek Dağılımı", fontsize=16)
plt.xlabel("Bölgeler", fontsize=14)
plt.ylabel("Yemek Sayısı", fontsize=14)
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()

# Kategorilere göre yemek sayısı
categories = [G.nodes[n]["category"] for n in G.nodes]
category_counts = pd.Series(categories).value_counts()

# Pasta grafiği
plt.figure(figsize=(8, 8))
category_counts.plot.pie(
    autopct="%1.1f%%", colors=plt.cm.Paired.colors, textprops={"fontsize": 12}, startangle=90
)
plt.title("Kategorilere Göre Yemek Dağılımı", fontsize=16)
plt.ylabel("")  # Y eksenini gizle
plt.show()

# Malzemelerin popülerlik analizi
ingredient_counts = {}
for _, _, data in G.edges(data=True):
    for ingredient in data["ortak_malzemeler"]:
        ingredient_counts[ingredient] = ingredient_counts.get(ingredient, 0) + 1

ingredient_df = pd.DataFrame(list(ingredient_counts.items()), columns=["Ingredient", "Count"])
ingredient_df = ingredient_df.sort_values("Count", ascending=False).head(10)  # İlk 10 malzeme

# Barplot ile görselleştirme
plt.figure(figsize=(10, 6))
sns.barplot(data=ingredient_df, x="Count", y="Ingredient", palette="viridis")
plt.title("En Çok Kullanılan Malzemeler", fontsize=16)
plt.xlabel("Kullanım Sayısı", fontsize=14)
plt.ylabel("Malzeme", fontsize=14)
plt.grid(axis="x", linestyle="--", alpha=0.7)
plt.show()



# Düğüm ve kenar koordinatları
pos = nx.spring_layout(G, seed=42)  # Sabit düzen için seed ekledik
x_nodes = [pos[n][0] for n in G.nodes]  # Düğüm X koordinatları
y_nodes = [pos[n][1] for n in G.nodes]  # Düğüm Y koordinatları

# Kenar koordinatlarını al
edge_x = []  # Kenar X koordinatları
edge_y = []  # Kenar Y koordinatları
edge_texts = []  # Kenar üzerindeki ortak malzeme etiketleri

for edge in G.edges(data=True):
    x0, y0 = pos[edge[0]]  # İlk düğümün koordinatları
    x1, y1 = pos[edge[1]]  # İkinci düğümün koordinatları
    edge_x += [x0, x1, None]  # Çizgi koordinatları (x)
    edge_y += [y0, y1, None]  # Çizgi koordinatları (y)

    # Ortak malzemeleri etiket olarak ekle
    ortak_malzemeler = ", ".join(edge[2].get("ortak_malzemeler", []))  # Ortak malzemeler
    edge_texts.append(ortak_malzemeler)

# Kenarları görselleştirme
edge_trace = go.Scatter(
    x=edge_x,
    y=edge_y,
    line=dict(width=1, color="gray"),  # Kenarların rengi ve genişliği
    hoverinfo="text",  # Hoverda bilgi göster
    mode="lines",  # Çizgi modu
    # text=edge_texts,  # Hover metni: Ortak malzemeler
    text=[f"Ortak Malzemeler: {malzeme}" for malzeme in edge_texts],
    name="Ortak Malzemeler"
)
# Düğümleri görselleştirme
node_trace = go.Scatter(
    x=x_nodes,
    y=y_nodes,
    mode="markers+text",
    text=[G.nodes[n]["name"] for n in G.nodes],  # Düğüm isimleri
    textposition="top center",  # İsimlerin pozisyonu
    marker=dict(size=10, color="blue", opacity=0.8),  # Düğüm renk ve boyutu
    name="Yemekler",
    hovertext=[  # Hover metni: Ortak malzemeler
        f"{G.nodes[node]['name']}<br>Kullandığı Malzemeler: " + 
        ", ".join(
            set(
                material
                for edge in G.edges(node, data=True)
                for material in edge[2].get("ortak_malzemeler", [])
            )
        )
        for node in G.nodes
    ], 
    hoverinfo="text",  # Hoverda sadece metin göster
)

# Haritayı görselleştirme
fig = go.Figure(data=[edge_trace, node_trace])
fig.update_layout(
    title="Türk Mutfağı Yemek Grafı",
    showlegend=False,
    xaxis=dict(showgrid=False, zeroline=False),
    yaxis=dict(showgrid=False, zeroline=False),
)
pio.renderers.default = "browser"
fig.show()

file_path = "/Users/sekerismail/Desktop/Turkish-Kitchen-NetworkX/dataset.json"
with open(file_path, "r", encoding="utf-8") as file:
    data2 = json.load(file)

G = nx.Graph()

# Düğümleri ekleme
for yemek in data2["nodes"]:
    G.add_node(
        yemek["id"],  # Düğüm kimliği
        name=yemek["name"],  # Yemek adı
        region=yemek["region"],  # Bölge
        category=yemek["category"],  # Kategori
        ingredients=yemek["ingredients"]  # Malzemeler
    )

# Kenarları oluşturma (ortak malzemelere göre bağlama)
for yemek1 in data2["nodes"]:
    for yemek2 in data2["nodes"]:
        if yemek1["id"] != yemek2["id"]:  # Aynı düğümü bağlamayın
            ortak_malzemeler = set(yemek1["ingredients"]) & set(yemek2["ingredients"])
            if ortak_malzemeler:  # Ortak malzeme varsa kenar oluştur
                G.add_edge(yemek1["id"], yemek2["id"], ortak_malzemeler=list(ortak_malzemeler))

# Harita verisini yükle
file_path = "/Users/sekerismail/Desktop/Turkish-Kitchen-NetworkX/custom.geo.json"
turkey_map = gpd.read_file(file_path)
sns.barplot(x=region_counts.keys(), y=region_counts.values(), palette='viridis', hue=region_counts.keys(), legend=False)


# 1. Yemeklerin Bölgelere Göre Sayısını Hesaplama
region_counts = Counter([yemek["region"] for yemek in data2["nodes"]])

region_df = pd.DataFrame(list(region_counts.items()), columns=['region', 'yemek_sayisi'])

# 2. Harita Üzerinde Yemek Sayısı Verisini Ekleme
# Türkiye haritasına yemek sayısı verilerini merge edin
turkey_map = turkey_map.merge(region_df, left_on='name', right_on='region', how='left')

# 3. NaN Değerlerini Doldurma
turkey_map['yemek_sayisi'] = turkey_map['yemek_sayisi'].fillna(0)  # NaN olanları 0 ile doldur

# 4. Yemek Sayısı Sütununun Veri Tipini Kontrol Etme ve Gerekirse Dönüştürme
turkey_map['yemek_sayisi'] = pd.to_numeric(turkey_map['yemek_sayisi'], errors='coerce')

# 5. Harita Üzerinde Görselleştirme
fig, ax = plt.subplots(1, 1, figsize=(12, 12))

# Harita sınırlarını çizin
turkey_map.boundary.plot(ax=ax, linewidth=1)

# Yemek sayısına göre bölgeleri renkli gösterin
turkey_map.plot(column='yemek_sayisi', ax=ax, legend=True,
               legend_kwds={'label': "Yemek Sayısı",
                            'orientation': "horizontal"},
               cmap='OrRd')  # OrRd renk paleti

# Başlık ekleyin    
plt.title("Türkiye Bölgelerinde Yemek Dağılımı")
plt.show()

import community as community_louvain
# Bir ağ (graph) oluşturun
G = nx.erdos_renyi_graph(100, 0.1)
# Louvain algoritması ile toplulukları tespit et
partition = community_louvain.best_partition(G)

# Sonuçları yazdıralım
print(partition)
# Toplulukları görselleştirelim
import matplotlib.pyplot as plt
# Her topluluğa farklı renk ver
colors = [partition[node] for node in G.nodes]
# Görselleştirme
plt.figure(figsize=(10, 7))
nx.draw(G, node_color=colors, with_labels=True, cmap=plt.cm.jet)
plt.title("Louvain Algoritması ile Topluluk Tespiti", fontsize=16)
plt.show()





