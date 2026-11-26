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
  safe: { flex: 1, backgroundColor: "#101411" },
  content: { padding: 22, paddingBottom: 48, maxWidth: 1100, width: "100%", alignSelf: "center" },
  header: { flexDirection: "row", alignItems: "center", justifyContent: "space-between", marginBottom: 28, gap: 12 },
  kicker: { color: "#a7c879", fontSize: 10, letterSpacing: 2, fontWeight: "700" },
  brand: { color: "#f1f3ec", fontSize: 22, fontWeight: "900", letterSpacing: 1.2, marginTop: 5 },
  brandAccent: { color: "#c5ed73" },
  platformPill: { borderWidth: 1, borderColor: "#344334", borderRadius: 20, paddingVertical: 8, paddingHorizontal: 11 },
  platformText: { color: "#aeb9ac", fontSize: 9, fontWeight: "700" },
  hero: { borderRadius: 18, borderWidth: 1, borderColor: "#354637", backgroundColor: "#19251d", padding: 24, marginBottom: 30 },
  heroEyebrow: { color: "#c5ed73", fontSize: 10, fontWeight: "800", letterSpacing: 2 },
  heroTitle: { color: "#f1f3ec", fontSize: 42, lineHeight: 44, fontWeight: "900", marginTop: 18 },
  heroBody: { color: "#b7c1b5", fontSize: 15, lineHeight: 23, marginTop: 16, maxWidth: 520 },
  disclaimer: { color: "#89968a", fontSize: 11, lineHeight: 17, marginTop: 18, maxWidth: 600 },
  sectionHeader: { marginBottom: 14 },
  sectionTitle: { color: "#f1f3ec", fontSize: 21, fontWeight: "800" },
  sectionSub: { color: "#89968a", fontSize: 12, marginTop: 4 },
  grid: { flexDirection: "row", flexWrap: "wrap", justifyContent: "space-between", gap: 12 },
  cardWrap: { minWidth: "47%" },
  card: { backgroundColor: "#171e19", borderColor: "#2b352e", borderWidth: 1, borderRadius: 14, padding: 17, minHeight: 154 },
  cardSymbol: { color: "#c5ed73", fontSize: 24, marginBottom: 14 },
  cardTitle: { color: "#f1f3ec", fontSize: 16, fontWeight: "800" },
  cardDetail: { color: "#9eaa9e", fontSize: 12, lineHeight: 18, marginTop: 7 },
  cardArrow: { color: "#c5ed73", fontSize: 9, fontWeight: "800", letterSpacing: 1, marginTop: 14 },
  footer: { color: "#687469", fontSize: 9, letterSpacing: 1, marginTop: 30, textAlign: "center" }
});
