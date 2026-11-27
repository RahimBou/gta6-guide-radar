import { Link, useLocalSearchParams } from "expo-router";
import { useCallback, useEffect, useState } from "react";
import { ActivityIndicator, Alert, Linking, Pressable, ScrollView, StyleSheet, Text, TextInput, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

const API = "https://gta6-guide-radar.onrender.com";
const config: Record<string,{title:string;intro:string;endpoint:string;empty:string}> = {
  map:{title:"Carte de Leonida",intro:"Marqueurs et lieux enregistrés dans la base du guide.",endpoint:"/api/map/markers",empty:"Aucun marqueur confirmé n'est encore enregistré."},
  discoveries:{title:"Astuces & découvertes",intro:"Fiches proposées par le robot à partir des sources ajoutées.",endpoint:"/api/robot/tips",empty:"Aucune fiche disponible. Ajoutez des sources vidéo dans Robot Radar."},
  vehicles:{title:"Véhicules",intro:"Fiches véhicules issues de la base documentaire.",endpoint:"/api/guide/entries?category=vehicle",empty:"Aucune fiche véhicule documentée pour le moment."},
  missions:{title:"Missions & activités",intro:"Guides et étapes documentés.",endpoint:"/api/guide/entries?category=mission",empty:"Aucune mission documentée pour le moment."},
  secrets:{title:"Secrets & collections",intro:"Secrets, objets et collections enregistrés.",endpoint:"/api/guide/entries?category=collectible",empty:"Aucun secret documenté pour le moment."},
  progress:{title:"Ma progression",intro:"Votre suivi local des modules et des découvertes.",endpoint:"/api/guide/entries",empty:"La progression sera alimentée à mesure que vous marquerez des fiches comme terminées."},
  robot:{title:"Robot Radar",intro:"Ajoutez une vidéo publique : le robot crée une tâche de contrôle et de traitement.",endpoint:"/api/robot/videos",empty:"Aucune source vidéo enregistrée."},
  sources:{title:"Sources & actualités",intro:"Liens et métadonnées issus des flux publics GTA VI. Chaque élément reste non vérifié jusqu’à contrôle.",endpoint:"/api/robot/items",empty:"Aucune actualité collectée. Le robot doit effectuer une recherche depuis le serveur."},
};

export default function SectionScreen() {
  const { section } = useLocalSearchParams<{section:string}>();
  const key = String(section || "map");
  const item = config[key] || config.map;
  const [rows,setRows] = useState<any[]>([]);
  const [loading,setLoading] = useState(true);
  const [error,setError] = useState("");
  const [url,setUrl] = useState("");
  const [title,setTitle] = useState("");
  const [saving,setSaving] = useState(false);

  const load = useCallback(async () => {
    setLoading(true); setError("");
    try {
      const response = await fetch(API + item.endpoint);
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || "API indisponible");
      setRows(Array.isArray(data.items) ? data.items : []);
    } catch (e:any) { setError(e.message || "Connexion impossible"); }
    finally { setLoading(false); }
  },[item.endpoint]);

  useEffect(()=>{load()},[load]);

  async function addVideo() {
    if (!url.trim()) { Alert.alert("Adresse manquante","Collez le lien d'une vidéo YouTube, TikTok ou Twitch."); return; }
    setSaving(true);
    try {
      const response = await fetch(API + "/api/robot/videos",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({url:url.trim(),title:title.trim()})});
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || "Enregistrement impossible");
      setUrl(""); setTitle("");
      Alert.alert("Source enregistrée","Une tâche de vérification des droits a été créée.");
      await load();
    } catch(e:any) { Alert.alert("Erreur",e.message || "Enregistrement impossible"); }
    finally { setSaving(false); }
  }

  return (
    <SafeAreaView style={styles.safe}>
      <ScrollView contentContainerStyle={styles.content}>
        <Link href="/" style={styles.back}>← ACCUEIL</Link>
        <Text style={styles.kicker}>GTA 6 GUIDE RADAR</Text>
        <Text style={styles.title}>{item.title}</Text>
        <Text style={styles.intro}>{item.intro}</Text>

        {key === "map" ? <Pressable onPress={()=>Linking.openURL("https://promptowy.com/fr/gta-6/carte-interactive/")} style={styles.button}><Text style={styles.buttonText}>OUVRIR LA CARTE INTERACTIVE COMPLÈTE ↗</Text></Pressable> : null}

        {key === "robot" ? <View style={styles.form}>
          <Text style={styles.formTitle}>AJOUTER UNE SOURCE VIDÉO</Text>
          <TextInput value={title} onChangeText={setTitle} placeholder="Titre de la vidéo (facultatif)" placeholderTextColor="#9f849e" style={styles.input}/>
          <TextInput value={url} onChangeText={setUrl} placeholder="https://www.youtube.com/…" placeholderTextColor="#9f849e" autoCapitalize="none" keyboardType="url" style={styles.input}/>
          <Pressable onPress={addVideo} disabled={saving} style={styles.button}>{saving?<ActivityIndicator color="#180e1c"/>:<Text style={styles.buttonText}>ENREGISTRER LA SOURCE ↗</Text>}</Pressable>
        </View> : null}

        {loading ? <ActivityIndicator color="#ff83bd" size="large" style={{marginTop:28}}/> :
          error ? <View style={styles.empty}><Text style={styles.emptyTitle}>Connexion indisponible</Text><Text style={styles.body}>{error}</Text><Pressable onPress={load} style={styles.retry}><Text style={styles.retryText}>RÉESSAYER</Text></Pressable></View> :
          rows.length===0 ? <View style={styles.empty}><Text style={styles.emptySymbol}>⌁</Text><Text style={styles.emptyTitle}>{item.empty}</Text><Text style={styles.body}>Aucune information n'est inventée : seules les données enregistrées et vérifiables sont affichées.</Text></View> :
          <View style={styles.list}>{rows.map((row,i)=>{
            const heading=row.title || row.name || "Élément sans titre";
            const sub=[row.category,row.status,row.platform,row.region,row.grid_ref].filter(Boolean).join(" · ");
            const detail=row.body || row.description || row.summary || row.message || row.url || "";
            return <View key={String(row.id || i)} style={styles.row}><Text style={styles.rowTitle}>{heading}</Text>{sub?<Text style={styles.meta}>{sub.toUpperCase()}</Text>:null}{detail?<Text style={styles.body}>{detail}</Text>:null}{row.url?<Pressable accessibilityRole="link" onPress={()=>Linking.openURL(row.url).catch(()=>Alert.alert("Lien indisponible","Impossible d’ouvrir cette adresse."))}><Text style={styles.linkText} numberOfLines={2}>OUVRIR LA SOURCE ↗</Text></Pressable>:null}</View>;
          })}</View>
        }
        <Text style={styles.footer}>LES DONNÉES SONT ACTUALISÉES DEPUIS LE SERVEUR GTA 6 GUIDE RADAR</Text>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles=StyleSheet.create({
 safe:{flex:1,backgroundColor:"#100d18"},content:{padding:22,paddingBottom:48,maxWidth:850,width:"100%",alignSelf:"center"},
 back:{color:"#ff83bd",fontSize:10,fontWeight:"900",letterSpacing:1.4,marginBottom:28},kicker:{color:"#f58bc5",fontSize:10,fontWeight:"900",letterSpacing:2},
 title:{color:"#fff9f7",fontSize:32,fontWeight:"900",marginTop:9},intro:{color:"#d8c5d7",fontSize:14,lineHeight:21,marginTop:10,marginBottom:24},
 form:{backgroundColor:"#211829",borderColor:"#70405f",borderWidth:1,borderRadius:15,padding:16,marginBottom:22},formTitle:{color:"#ff83bd",fontSize:10,fontWeight:"900",letterSpacing:1.5,marginBottom:12},
 input:{backgroundColor:"#130f1b",borderColor:"#49324f",borderWidth:1,borderRadius:9,padding:13,color:"#fff9f7",fontSize:14,marginBottom:10},
 button:{backgroundColor:"#ff83bd",borderRadius:9,padding:14,alignItems:"center",minHeight:46,justifyContent:"center"},buttonText:{color:"#1a101d",fontWeight:"900",fontSize:11,letterSpacing:1},
 empty:{backgroundColor:"#211829",borderColor:"#49324f",borderWidth:1,borderRadius:15,padding:22,marginTop:12},emptySymbol:{color:"#ff83bd",fontSize:30},emptyTitle:{color:"#fff9f7",fontSize:17,fontWeight:"900",lineHeight:24,marginTop:7},body:{color:"#d0b9d0",fontSize:13,lineHeight:20,marginTop:9},
 retry:{alignSelf:"flex-start",marginTop:16,paddingVertical:10,paddingHorizontal:15,borderWidth:1,borderColor:"#ff83bd",borderRadius:8},retryText:{color:"#ff83bd",fontSize:10,fontWeight:"900"},
 list:{gap:10},row:{backgroundColor:"#211829",borderColor:"#49324f",borderWidth:1,borderRadius:13,padding:15},rowTitle:{color:"#fff9f7",fontSize:16,fontWeight:"900"},meta:{color:"#ff83bd",fontSize:9,fontWeight:"900",letterSpacing:1,marginTop:6},linkText:{color:"#dba8c9",fontSize:11,marginTop:8},footer:{color:"#9e809b",fontSize:9,letterSpacing:1,textAlign:"center",marginTop:30}
});
