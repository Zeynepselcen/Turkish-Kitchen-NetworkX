import json
import networkx as nx
import matplotlib.pyplot as plt

# JSON dosyasını yükleme
# file_path = "C:/Users/Lenovo/Desktop/SNA/Turkish-Kitchen-NetworkX/yemeklerr.json"
file_path = "/Users/sekerismail/Desktop/Turkish-Kitchen-NetworkX/yemeklerr.json"
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
        ingredients=yemek["ingredients"],  # Malzemeler
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


# Grafiği görselleştirme
plt.figure(figsize=(12, 12))
nx.draw(
    G,
    pos=pos,
    with_labels=True,
    node_size=3000,
    font_size=10,
    node_color="lightgreen",
    font_weight="bold",
    edge_color="gray",
    alpha=0.8
)
plt.title("Türk Mutfağı Yemek Grafiği")
plt.show()

# DERECE DAGİLİMİ NE ISE YARAR
# Ne İşe Yarar?: Yemeklerin komşu sayılarının (derece) dağılımını görürsünüz. Hangi yemeklerin daha merkezi olduğunu veya popüler olduğunu anlamak için kullanılabilir.
degrees = [degree for _, degree in G.degree()]
plt.hist(degrees, bins=range(1, max(degrees) + 2), align='left', color='skyblue', edgecolor='black')
plt.title("Düğüm Dereceleri Dağılımı")
plt.xlabel("Komşu Sayısı (Derece)")
plt.ylabel("Düğüm Sayısı")
plt.show()

# Kümeleme Katsayısı (Clustering Coefficient)
# Ne İşe Yarar?: Her yemeğin, komşuları arasındaki bağlantıların ne kadar yoğun olduğunu gösterir. Komşu yemeklerin ne kadar birbirine benzediğini anlamak için kullanılabilir.

clustering = nx.clustering(G)  # Her düğüm için kümeleme katsayısı
average_clustering = nx.average_clustering(G)  # Tüm grafın ortalama kümeleme katsayısı
print(f"Ortalama Kümeleme Katsayısı: {average_clustering}")

# En yüksek kümeleme katsayısına sahip 5 düğüm
top_clustering = sorted(clustering.items(), key=lambda x: x[1], reverse=True)[:5]
print("En yüksek kümeleme katsayısına sahip düğümler:")
for node, coef in top_clustering:
    print(f"Yemek ID: {node}, Adı: {G.nodes[node]['name']}, Kümeleme Katsayısı: {coef}")
# Bağlantı Bileşenleri (Connected Components)
# Ne İşe Yarar?: Grafın ayrık (bağımsız) parçalarını bulur. Yemekler arasında bağlantısı olmayan alt grupları analiz etmek için kullanılabilir.
components = list(nx.connected_components(G))
print(f"Graf, {len(components)} farklı bağlantılı bileşene sahiptir.")

# Her bileşenin düğümlerini yazdırma
for i, component in enumerate(components):
    print(f"Bileşen {i + 1}: {component}")
# Merkezilik Ölçümleri (Centrality Measures)
# Ne İşe Yarar?: Hangi yemeklerin grafikte daha merkezi bir rol oynadığını bulur. Daha fazla bağlantıya sahip veya stratejik pozisyondaki yemekleri belirlemek için kullanılabilir.
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
# Ne İşe Yarar?: İki yemek arasındaki bağlantıların en kısa yolunu bulur. Yemekler arasında hangi malzemelerin köprü rolü oynadığını anlamak için kullanılabilir.

source = 1  # Kaynak düğüm ID'si
target = 48  # Hedef düğüm ID'si
if nx.has_path(G, source, target):
    path = nx.shortest_path(G, source=source, target=target)
    print(f"En kısa yol ({source} -> {target}): {path}")
else:
    print(f"{source} ve {target} arasında yol yok.")

# Çap (Diameter)
# Ne İşe Yarar?: Grafın en uzak iki düğümü arasındaki yol uzunluğunu bulur. Grafın "genişliğini" anlamak için kullanılır.

if nx.is_connected(G):
    diameter = nx.diameter(G)
    print(f"Grafın çapı (en uzun en kısa yol): {diameter}")
else:
    print("Graf bağlantılı değil, çap hesaplanamaz.")

# Topluluk Algılama (Community Detection)
# Ne İşe Yarar?: Grafı benzer özelliklere sahip alt gruplara (topluluklara) böler. Yemeklerin benzer malzemelere göre hangi topluluklarda gruplaştığını görmek için kullanılabilir.
# Girvan-Newman Algorithm

from networkx.algorithms.community import girvan_newman

communities = next(girvan_newman(G))  # İlk topluluk bölünmesini al
for i, community in enumerate(communities):
    print(f"Topluluk {i + 1}: {sorted(community)}")

# Yoğunluk (Density)
# Ne İşe Yarar?: Grafın ne kadar yoğun bağlantıya sahip olduğunu ölçer. Yemeklerin birbirine ne kadar bağlı olduğunu anlamak için kullanılabilir.

density = nx.density(G)
print(f"Grafın yoğunluğu: {density}")
# Yemekler Arası Benzerlik Skoru
# Ne yapar?: Yemekler arasındaki benzerliği, kullanılan malzemelere göre bir "skor" ile ifade edebilirsiniz. Örneğin, iki yemek ne kadar fazla ortak malzeme içeriyorsa, aralarındaki skor o kadar yüksek olabilir.

from networkx.algorithms.link_prediction import jaccard_coefficient
# Jaccard skorlarını hesaplama
for u, v, p in jaccard_coefficient(G, [(y1, y2) for y1 in G.nodes for y2 in G.nodes if y1 != y2]):
    yemek1_name = G.nodes[u]["name"]
    yemek2_name = G.nodes[v]["name"]
    
    print(f"Yemek {yemek1_name} ile Yemek {yemek2_name} arasındaki Jaccard Skoru: {p:.2f}")


