import { useEffect, useMemo, useState } from "react";
import { ActivityIndicator, Linking, Pressable, ScrollView, StyleSheet, Text, TextInput, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

const API = "https://gta6-guide-radar.onrender.com";
type GuideEntry = {
  id: string; title: string; summary: string; body: string; category: string;
  status: string; region?: string | null; source_url?: string | null; source_label?: string | null;
};

const filters = [
  { id: "all", label: "Tout" },
  { id: "region", label: "Régions" },
  { id: "base_radar", label: "Bases radar" },
  { id: "weapon", label: "Armes" },
  { id: "mission", label: "Missions" },
  { id: "vehicle", label: "Véhicules" },
  { id: "collectible", label: "Secrets" },
  { id: "tip", label: "Astuces" },
];

export default function GuidesScreen() {
  const [items, setItems] = useState<GuideEntry[]>([]);
  const [filter, setFilter] = useState("all");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [query, setQuery] = useState("");

  useEffect(() => {
    let active = true;
    fetch(API + "/api/guide/entries")
      .then(async response => {
        if (!response.ok) throw new Error("Le serveur de guides est momentanément indisponible.");
        return response.json();
      })
      .then(data => { if (active) setItems(Array.isArray(data.items) ? data.items : []); })
      .catch(err => { if (active) setError(err.message || "Erreur de connexion."); })
      .finally(() => { if (active) setLoading(false); });
    return () => { active = false; };
  }, []);

  const visible = useMemo(() => items.filter(item => (filter === "all" || item.category === filter) && (item.title + " " + item.summary + " " + (item.region || "")).toLowerCase().includes(query.toLowerCase().trim())), [items, filter, query]);

  return (
    <SafeAreaView style={styles.safe}>
      <ScrollView contentContainerStyle={styles.content}>
        <Text style={styles.kicker}>BASE DOCUMENTAIRE · LEONIDA</Text>
        <Text style={styles.title}>Fiches & lieux</Text>
        <Text style={styles.intro}>Régions, bases radar et équipements recensés à partir de guides publics. Chaque fiche conserve sa source et son statut.</Text>
        <TextInput value={query} onChangeText={setQuery} placeholder="Rechercher une mission, un lieu, une arme…" placeholderTextColor="#9e809b" style={styles.search} />
        <View style={styles.filters}>
          {filters.map(item => (
            <Pressable key={item.id} onPress={() => setFilter(item.id)} style={[styles.filter, filter === item.id && styles.filterActive]}>
              <Text style={[styles.filterText, filter === item.id && styles.filterTextActive]}>{item.label}</Text>
            </Pressable>
          ))}
        </View>
        {loading ? <ActivityIndicator color="#ff83bd" size="large" style={{marginTop:30}} /> : null}
        {error ? <View style={styles.notice}><Text style={styles.noticeText}>{error}</Text><Pressable onPress={() => {setLoading(true);setError("");fetch(API + "/api/guide/entries").then(r=>r.json()).then(d=>setItems(d.items||[])).catch(e=>setError(e.message)).finally(()=>setLoading(false));}}><Text style={styles.retry}>RÉESSAYER</Text></Pressable></View> : null}
        {!loading && !error && visible.length === 0 ? <Text style={styles.empty}>Aucune fiche dans cette catégorie pour le moment.</Text> : null}
        {!loading && !error ? <Text style={styles.count}>{visible.length} fiche(s) affichée(s)</Text> : null}
        {visible.map(item => (
          <View key={item.id} style={styles.card}>
            <View style={styles.metaRow}>
              <Text style={styles.category}>{item.category.replace("_", " ").toUpperCase()}</Text>
              <Text style={styles.status}>{item.status === "source_pending" ? "SOURCE À COMPLÉTER" : "À VÉRIFIER"}</Text>
            </View>
            <Text style={styles.cardTitle}>{item.title}</Text>
            {item.region ? <Text style={styles.region}>{item.region}</Text> : null}
            <Text style={styles.summary}>{item.summary}</Text>
            <Text style={styles.body}>{item.body}</Text>
            {item.source_url ? <Pressable onPress={() => Linking.openURL(item.source_url!)}><Text style={styles.source}>SOURCE : {item.source_label || "Ouvrir le guide"} ↗</Text></Pressable> : null}
          </View>
        ))}
        <Text style={styles.footer}>GTA 6 GUIDE RADAR · PROJET INDÉPENDANT</Text>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe:{flex:1,backgroundColor:"#100d18"},
  content:{padding:16,paddingBottom:40,maxWidth:900,width:"100%",alignSelf:"center"},
  kicker:{color:"#f58bc5",fontSize:9,fontWeight:"900",letterSpacing:2,marginTop:8},
  title:{color:"#fff9f7",fontSize:30,fontWeight:"900",marginTop:7},
  intro:{color:"#d0b9d0",fontSize:13,lineHeight:19,marginTop:7},
  search:{backgroundColor:"#1c1227",borderWidth:1,borderColor:"#55345f",borderRadius:10,color:"#fff9f7",padding:12,fontSize:12,marginTop:15},
  count:{color:"#ff9acb",fontSize:10,fontWeight:"900",marginBottom:10},
  filters:{flexDirection:"row",flexWrap:"wrap",gap:7,marginVertical:16},
  filter:{borderWidth:1,borderColor:"#55345f",borderRadius:20,paddingVertical:8,paddingHorizontal:12,backgroundColor:"#1c1227"},
  filterActive:{backgroundColor:"#542344",borderColor:"#f58bc5"},
  filterText:{color:"#d0b9d0",fontSize:10,fontWeight:"800"},
  filterTextActive:{color:"#fff4f8"},
  card:{backgroundColor:"#211829",borderColor:"#4b344f",borderWidth:1,borderRadius:14,padding:15,marginBottom:11},
  metaRow:{flexDirection:"row",justifyContent:"space-between",gap:8},
  category:{color:"#ffb0d0",fontSize:9,fontWeight:"900",letterSpacing:1},
  status:{color:"#ffcf8b",fontSize:8,fontWeight:"900"},
  cardTitle:{color:"#fff9f7",fontSize:19,fontWeight:"900",marginTop:8},
  region:{color:"#ff9acb",fontSize:10,fontWeight:"800",marginTop:3},
  summary:{color:"#f2dfea",fontSize:13,fontWeight:"700",lineHeight:19,marginTop:8},
  body:{color:"#d0b9d0",fontSize:12,lineHeight:18,marginTop:8},
  source:{color:"#ff9acb",fontSize:10,fontWeight:"900",marginTop:13},
  empty:{color:"#d0b9d0",fontSize:13,textAlign:"center",marginTop:28},
  notice:{padding:14,borderRadius:12,backgroundColor:"#32182c",marginTop:18},
  noticeText:{color:"#f2dfea",fontSize:12},
  retry:{color:"#ff9acb",fontWeight:"900",fontSize:10,marginTop:12},
  footer:{color:"#9e809b",fontSize:9,letterSpacing:.5,marginTop:22,textAlign:"center"}
});
