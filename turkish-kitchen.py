import json
import networkx as nx
import matplotlib.pyplot as plt

file_path = "/Users/sekerismail/Desktop/networkx/yemekler-2.json"
with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

G = nx.Graph()

if isinstance(data.get("nodes"), list):
    for yemek in data["nodes"]:
        if isinstance(yemek, dict):  
            G.add_node(
                yemek["id"],
                name=yemek["name"],
                region=yemek["region"],
                category=yemek["category"],
                ingredients=yemek["ingredients"],
                description=yemek["description"]
            )
        else:
            print(f"Hata: {yemek} bir sözlük değil.")
else:
    print("'nodes' anahtarı bir liste değil, kontrol edilmesi gerekebilir.")

for yemek1 in data["nodes"]:
    if isinstance(yemek1, dict):  
        for yemek2 in data["nodes"]:
            if isinstance(yemek2, dict) and yemek1["id"] != yemek2["id"]: 
                ortak_malzemeler = set(yemek1["ingredients"]) & set(yemek2["ingredients"])
                if ortak_malzemeler:  
                    G.add_edge(yemek1["id"], yemek2["id"], ortak_malzemeler=list(ortak_malzemeler))

plt.figure(figsize=(12, 12))
nx.draw(
    G, 
    with_labels=True, 
    node_size=3000, 
    font_size=10, 
    node_color="skyblue", 
    font_weight="bold", 
    alpha=0.7
)
plt.title("Türk Mutfağı Yemekleri Grafiği")
plt.show()
