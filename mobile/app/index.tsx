import { Link } from "expo-router";
import { ScrollView, StyleSheet, Text, View, useWindowDimensions } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

const sections = [
  { title: "Carte de Leonida", detail: "Explorer les lieux et marqueurs vérifiés.", href: "/map", symbol: "⌖" },
  { title: "Découvertes", detail: "Retrouver les fiches et astuces documentées.", href: "/discoveries", symbol: "✳" },
  { title: "Véhicules", detail: "Consulter les véhicules et leurs informations.", href: "/vehicles", symbol: "▰" },
  { title: "Missions", detail: "Suivre les missions et activités.", href: "/missions", symbol: "◈" },
  { title: "Secrets & collections", detail: "Organiser les éléments à découvrir.", href: "/secrets", symbol: "⌁" },
  { title: "Ma progression", detail: "Retrouver favoris et éléments terminés.", href: "/progress", symbol: "◴" },
] as const;

export default function HomeScreen() {
  const { width } = useWindowDimensions();
  const columns = width >= 760 ? 2 : 1;

  return (
    <SafeAreaView style={styles.safe}>
      <ScrollView contentContainerStyle={styles.content}>
        <View style={styles.header}>
          <View>
            <Text style={styles.kicker}>COMPAGNON INDÉPENDANT</Text>
            <Text style={styles.brand}>LEONIDA <Text style={styles.brandAccent}>RADAR</Text></Text>
          </View>
          <View style={styles.platformPill}><Text style={styles.platformText}>PS5 · XBOX SERIES</Text></View>
        </View>
        <View style={styles.hero}>
          <Text style={styles.heroEyebrow}>GTA 6 GUIDE RADAR</Text>
          <Text style={styles.heroTitle}>Explorez.{"\n"}Repérez.{"\n"}Progressez.</Text>
          <Text style={styles.heroBody}>Votre compagnon d'exploration : carte interactive, fiches documentées et suivi personnel.</Text>
          <Text style={styles.disclaimer}>Projet indépendant, non affilié à Rockstar Games. Les informations seront publiées avec leur statut de vérification.</Text>
        </View>
        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>Votre espace de jeu</Text>
          <Text style={styles.sectionSub}>Choisissez un module</Text>
        </View>
        <View style={styles.grid}>
          {sections.map((item) => (
            <View key={item.href} style={[styles.cardWrap, { width: columns === 2 ? "48.5%" : "100%" }]}>
              <Link href={item.href} style={styles.card}>
                <Text style={styles.cardSymbol}>{item.symbol}</Text>
                <Text style={styles.cardTitle}>{item.title}</Text>
                <Text style={styles.cardDetail}>{item.detail}</Text>
                <Text style={styles.cardArrow}>OUVRIR ↗</Text>
              </Link>
            </View>
          ))}
        </View>
        <Text style={styles.footer}>GTA 6 GUIDE RADAR · VERSION 0.1.0 · APERÇU DE DÉVELOPPEMENT</Text>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: "#170522" },
  content: { padding: 22, paddingBottom: 48, maxWidth: 1100, width: "100%", alignSelf: "center" },
  header: { flexDirection: "row", alignItems: "center", justifyContent: "space-between", marginBottom: 28, gap: 12 },
  kicker: { color: "#ffadbf", fontSize: 10, letterSpacing: 2, fontWeight: "700" },
  brand: { color: "#fff9f7", fontSize: 22, fontWeight: "900", letterSpacing: 1.2, marginTop: 5 },
  brandAccent: { color: "#f58bc5" },
  platformPill: { borderWidth: 1, borderColor: "#68446d", borderRadius: 20, paddingVertical: 8, paddingHorizontal: 11 },
  platformText: { color: "#d0b9d0", fontSize: 9, fontWeight: "700" },
  hero: { borderRadius: 18, borderWidth: 1, borderColor: "#a65386", backgroundColor: "#38204f", padding: 24, marginBottom: 30 },
  heroEyebrow: { color: "#f58bc5", fontSize: 10, fontWeight: "800", letterSpacing: 2 },
  heroTitle: { color: "#fff9f7", fontSize: 42, lineHeight: 44, fontWeight: "900", marginTop: 18 },
  heroBody: { color: "#f0d9e7", fontSize: 15, lineHeight: 23, marginTop: 16, maxWidth: 520 },
  disclaimer: { color: "#cbb6ce", fontSize: 11, lineHeight: 17, marginTop: 18, maxWidth: 600 },
  sectionHeader: { marginBottom: 14 },
  sectionTitle: { color: "#fff9f7", fontSize: 21, fontWeight: "800" },
  sectionSub: { color: "#cbb6ce", fontSize: 12, marginTop: 4 },
  grid: { flexDirection: "row", flexWrap: "wrap", justifyContent: "space-between", gap: 12 },
  cardWrap: { minWidth: "47%" },
  card: { backgroundColor: "#2a1538", borderColor: "#55345f", borderWidth: 1, borderRadius: 14, padding: 17, minHeight: 154 },
  cardSymbol: { color: "#f58bc5", fontSize: 24, marginBottom: 14 },
  cardTitle: { color: "#fff9f7", fontSize: 16, fontWeight: "800" },
  cardDetail: { color: "#d0b9d0", fontSize: 12, lineHeight: 18, marginTop: 7 },
  cardArrow: { color: "#f58bc5", fontSize: 9, fontWeight: "800", letterSpacing: 1, marginTop: 14 },
  footer: { color: "#a77c9f", fontSize: 9, letterSpacing: 1, marginTop: 30, textAlign: "center" }
});
