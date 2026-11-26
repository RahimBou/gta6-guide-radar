import { Link, useLocalSearchParams } from "expo-router";
import { StyleSheet, Text, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

const titles: Record<string, string> = {
  map: "Carte de Leonida",
  discoveries: "Découvertes",
  vehicles: "Véhicules",
  missions: "Missions & activités",
  secrets: "Secrets & collections",
  progress: "Ma progression",
};

export default function ModulePlaceholderScreen() {
  const { section } = useLocalSearchParams<{ section: string }>();
  const title = titles[section] ?? "Module";

  return (
    <SafeAreaView style={styles.safe}>
      <View style={styles.content}>
        <Text style={styles.kicker}>GTA 6 GUIDE RADAR</Text>
        <Text style={styles.title}>{title}</Text>
        <Text style={styles.body}>Ce module est prévu dans l'architecture mobile. Son interface et ses données seront intégrées lors des prochaines phases de développement.</Text>
        <Text style={styles.note}>Aucun lieu ni contenu fictif n'est affiché.</Text>
        <Link href="/" style={styles.back}>← Retour à l'accueil</Link>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: "#0a1020" },
  content: { flex: 1, justifyContent: "center", padding: 28, maxWidth: 720, width: "100%", alignSelf: "center" },
  kicker: { color: "#ff82ad", fontSize: 10, fontWeight: "800", letterSpacing: 2 },
  title: { color: "#fff4ef", fontSize: 32, fontWeight: "900", marginTop: 12 },
  body: { color: "#c2c9d8", fontSize: 15, lineHeight: 23, marginTop: 18 },
  note: { color: "#9aa8bd", fontSize: 12, marginTop: 14 },
  back: { color: "#ff82ad", fontWeight: "800", marginTop: 28 }
});
