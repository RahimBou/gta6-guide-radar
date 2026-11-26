import { Link } from "expo-router";
import { useEffect, useState } from "react";
import { ActivityIndicator, ScrollView, StyleSheet, Text, View, useWindowDimensions } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

const API = "https://gta6-guide-radar.onrender.com";
const sections = [
  { title: "Carte de Leonida", detail: "Explorer les lieux et marqueurs disponibles.", href: "/map", symbol: "⌖" },
  { title: "Astuces & découvertes", detail: "Consulter les fiches issues des sources vidéo.", href: "/discoveries", symbol: "✳" },
  { title: "Véhicules", detail: "Retrouver les informations sur les véhicules.", href: "/vehicles", symbol: "▰" },
  { title: "Missions", detail: "Suivre les guides et étapes documentés.", href: "/missions", symbol: "◈" },
  { title: "Secrets & collections", detail: "Centraliser les éléments à découvrir.", href: "/secrets", symbol: "⌁" },
  { title: "Ma progression", detail: "Retrouver votre suivi personnel.", href: "/progress", symbol: "◴" },
  { title: "Robot Radar", detail: "Sources vidéo, analyse et fiches proposées.", href: "/robot", symbol: "◎" },
  { title: "Sources & actualités", detail: "Articles publics, guides et nouveautés collectés.", href: "/sources", symbol: "▤" },
] as const;

export default function HomeScreen() {
  const { width } = useWindowDimensions();
  const [stats, setStats] = useState<{videos:number; waiting:number; tips:number; published:number} | null>(null);
  const [apiError, setApiError] = useState(false);
  const columns = width >= 760 ? 2 : 1;

  useEffect(() => {
    let alive = true;
    fetch(API + "/api/robot/overview").then(r => { if (!r.ok) throw new Error("api"); return r.json(); })
      .then(data => { if (alive) { setStats(data); setApiError(false); } })
      .catch(() => { if (alive) setApiError(true); });
    return () => { alive = false; };
  }, []);

  return (
    <SafeAreaView style={styles.safe}>
      <ScrollView contentContainerStyle={styles.content}>
        <View style={styles.header}>
          <View><Text style={styles.kicker}>COMPAGNON INDÉPENDANT</Text><Text style={styles.brand}>GTA 6 <Text style={styles.brandAccent}>RADAR</Text></Text></View>
          <View style={styles.platformPill}><Text style={styles.platformText}>ANDROID · MOBILE</Text></View>
        </View>
        <View style={styles.hero}>
          <Text style={styles.heroEyebrow}>VICE CITY · LEONIDA</Text>
          <Text style={styles.heroTitle}>Explorez.{ "\n" }Repérez.{ "\n" }Progressez.</Text>
          <Text style={styles.heroBody}>Votre guide de jeu : carte, missions, astuces, véhicules et découvertes réunis dans une application mobile.</Text>
          <Text style={styles.disclaimer}>Projet indépendant, non affilié à Rockstar Games. Les informations sont distinguées selon leur niveau de vérification.</Text>
        </View>
        <View style={styles.stats}>
          <View style={styles.stat}><Text style={styles.statValue}>{stats ? stats.videos : "—"}</Text><Text style={styles.statLabel}>SOURCES VIDÉO</Text></View>
          <View style={styles.stat}><Text style={styles.statValue}>{stats ? stats.tips : "—"}</Text><Text style={styles.statLabel}>FICHES ROBOT</Text></View>
          <View style={styles.stat}><Text style={styles.statValue}>{stats ? stats.published : "—"}</Text><Text style={styles.statLabel}>PUBLIÉES</Text></View>
        </View>
        <Text style={styles.api}>{apiError ? "● ROBOT HORS LIGNE — MODE APPLICATION DISPONIBLE" : stats ? "● ROBOT CONNECTÉ" : "○ CONNEXION AU ROBOT…"}</Text>
        <View style={styles.sectionHeader}><Text style={styles.sectionTitle}>Votre espace de jeu</Text><Text style={styles.sectionSub}>Tous les modules au même endroit</Text></View>
        <View style={styles.grid}>
          {sections.map(item => (
            <View key={item.href} style={[styles.cardWrap, { width: columns === 2 ? "48.5%" : "100%" }]}>
              <Link href={item.href} style={styles.card}>
                <Text style={styles.cardSymbol}>{item.symbol}</Text><Text style={styles.cardTitle}>{item.title}</Text>
                <Text style={styles.cardDetail}>{item.detail}</Text><Text style={styles.cardArrow}>OUVRIR ↗</Text>
              </Link>
            </View>
          ))}
        </View>
        <Text style={styles.footer}>GTA 6 GUIDE RADAR · APPLICATION MOBILE</Text>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe:{flex:1,backgroundColor:"#100d18"},content:{padding:20,paddingBottom:48,maxWidth:1100,width:"100%",alignSelf:"center"},
  header:{flexDirection:"row",alignItems:"center",justifyContent:"space-between",marginBottom:22,gap:10},
  kicker:{color:"#f58bc5",fontSize:10,letterSpacing:2,fontWeight:"800"},brand:{color:"#fff9f7",fontSize:23,fontWeight:"900",letterSpacing:1.2,marginTop:5},brandAccent:{color:"#ff83bd"},
  platformPill:{borderWidth:1,borderColor:"#78415f",borderRadius:20,paddingVertical:8,paddingHorizontal:10},platformText:{color:"#f2c8df",fontSize:9,fontWeight:"800"},
  hero:{borderRadius:20,borderWidth:1,borderColor:"#a94d83",backgroundColor:"#28152f",padding:24,marginBottom:16},
  heroEyebrow:{color:"#ff83bd",fontSize:10,fontWeight:"900",letterSpacing:2},heroTitle:{color:"#fff9f7",fontSize:43,lineHeight:45,fontWeight:"900",marginTop:17},
  heroBody:{color:"#f0d9e7",fontSize:15,lineHeight:23,marginTop:15,maxWidth:540},disclaimer:{color:"#cbb6ce",fontSize:11,lineHeight:17,marginTop:17},
  stats:{flexDirection:"row",gap:9,marginBottom:12},stat:{flex:1,backgroundColor:"#1b1523",borderColor:"#453047",borderWidth:1,borderRadius:12,padding:13},statValue:{color:"#fff9f7",fontSize:23,fontWeight:"900"},statLabel:{color:"#c9a7bd",fontSize:8,letterSpacing:1,marginTop:4,fontWeight:"800"},
  api:{color:"#e9a6cb",fontSize:9,letterSpacing:1,fontWeight:"800",marginBottom:24},sectionHeader:{marginBottom:13},sectionTitle:{color:"#fff9f7",fontSize:21,fontWeight:"900"},sectionSub:{color:"#cbb6ce",fontSize:12,marginTop:4},
  grid:{flexDirection:"row",flexWrap:"wrap",justifyContent:"space-between",gap:11},cardWrap:{minWidth:"47%"},card:{backgroundColor:"#211829",borderColor:"#4b344f",borderWidth:1,borderRadius:14,padding:16,minHeight:150},
  cardSymbol:{color:"#ff83bd",fontSize:24,marginBottom:12},cardTitle:{color:"#fff9f7",fontSize:16,fontWeight:"900"},cardDetail:{color:"#d0b9d0",fontSize:12,lineHeight:18,marginTop:6},cardArrow:{color:"#ff83bd",fontSize:9,fontWeight:"900",letterSpacing:1,marginTop:13},
  footer:{color:"#a77c9f",fontSize:9,letterSpacing:1,marginTop:28,textAlign:"center"}
});
