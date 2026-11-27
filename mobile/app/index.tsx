import { Link } from "expo-router";
import { useRef, useState } from "react";
import { Image, PanResponder, Pressable, ScrollView, StyleSheet, Text, View, useWindowDimensions } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

const MAP_IMAGE = "https://guides-gta6.com/media/map/leonida-official.jpg";
const regions = [
  { id:"kalaga",name:"Mount Kalaga",county:"Lummox County",x:48,y:14,description:"Forêts, canyons et vallées au nord de Leonida." },
  { id:"gellhorn",name:"Port Gellhorn",county:"Kelly County",x:29,y:39,description:"Côte ouest, motels, port et routes secondaires." },
  { id:"ambrosia",name:"Ambrosia",county:"Leonard County",x:52,y:39,description:"Région intérieure autour du lac Leonida et de la raffinerie." },
  { id:"grassrivers",name:"Grassrivers",county:"Mariana County",x:45,y:66,description:"Marécages, mangroves et voies d’eau." },
  { id:"vicecity",name:"Vice City",county:"Vice-Dale County",x:64,y:53,description:"La grande métropole côtière de Leonida." },
  { id:"keys",name:"Leonida Keys",county:"Mariana County",x:51,y:82,description:"Archipel tropical et longues routes sur l’eau." },
] as const;

const sections = [
  { title:"Missions",detail:"Guides et étapes documentés.",href:"/missions",symbol:"◈" },
  { title:"Astuces & découvertes",detail:"Conseils et découvertes.",href:"/discoveries",symbol:"✳" },
  { title:"Véhicules",detail:"Catalogue des véhicules.",href:"/vehicles",symbol:"▰" },
  { title:"Secrets & collections",detail:"Objets et éléments à trouver.",href:"/secrets",symbol:"⌁" },
  { title:"Ma progression",detail:"Suivre les éléments terminés.",href:"/progress",symbol:"◴" },
] as const;

export default function HomeScreen() {
  const { width } = useWindowDimensions();
  const [selected,setSelected] = useState<string>("vicecity");
  const [zoom,setZoom] = useState(1);
  const [offset,setOffset] = useState({x:0,y:0});
  const gesture = useRef({x:0,y:0,baseDistance:0,baseZoom:1});
  const region = regions.find(r=>r.id===selected) || regions[0];
  const mapWidth = Math.min(width-32,620);
  const mapHeight = mapWidth/(731/1000);
  const clampZoom = (value:number) => Math.max(1,Math.min(3,value));
  const panResponder = useRef(PanResponder.create({
    onStartShouldSetPanResponder: () => true,
    onMoveShouldSetPanResponder: () => true,
    onPanResponderGrant: (evt) => {
      const t = evt.nativeEvent.touches;
      gesture.current = {x:offset.x,y:offset.y,baseDistance:t.length>1?Math.hypot(t[0].pageX-t[1].pageX,t[0].pageY-t[1].pageY):0,baseZoom:zoom};
    },
    onPanResponderMove: (evt,gs) => {
      const t = evt.nativeEvent.touches;
      if (t.length>1) {
        const d = Math.hypot(t[0].pageX-t[1].pageX,t[0].pageY-t[1].pageY);
        if (gesture.current.baseDistance>0) setZoom(clampZoom(gesture.current.baseZoom*d/gesture.current.baseDistance));
      } else if (zoom>1) {
        setOffset({x:gesture.current.x+gs.dx,y:gesture.current.y+gs.dy});
      }
    },
    onPanResponderRelease: () => {
      if (zoom<=1) setOffset({x:0,y:0});
    },
    onPanResponderTerminationRequest: () => false
  })).current;
  return (
    <SafeAreaView style={styles.safe}>
      <ScrollView contentContainerStyle={styles.content}>
        <View style={styles.header}>
          <View><Text style={styles.kicker}>COMPAGNON INDÉPENDANT</Text><Text style={styles.brand}>GTA 6 <Text style={styles.brandAccent}>GUIDE RADAR</Text></Text></View>
          <Text style={styles.platformPill}>LEONIDA · VI</Text>
        </View>

        <View style={styles.mapHeading}>
          <View><Text style={styles.heroEyebrow}>EXPLORE LE MONDE</Text><Text style={styles.title}>Carte interactive</Text></View>
          <Link href="/map" style={styles.fullMap}>GRANDE CARTE ↗</Link>
        </View>
        <Text style={styles.mapIntro}>Choisis une région directement sur la carte de Leonida.</Text>

        <View style={[styles.mapShell,{width:mapWidth,height:mapHeight}]} {...panResponder.panHandlers}>
          <View style={[styles.mapCanvas,{transform:[{translateX:offset.x},{translateY:offset.y},{scale:zoom}],width:mapWidth,height:mapHeight}]}>
            <Image source={{uri:MAP_IMAGE}} style={styles.mapImage} resizeMode="stretch" />
            {regions.map((r,i)=>(
              <Pressable key={r.id} onPress={()=>setSelected(r.id)} accessibilityRole="button" accessibilityLabel={"Sélectionner "+r.name}
                style={[styles.pin,{left:r.x+"%",top:r.y+"%"},selected===r.id&&styles.pinActive]}>
                <Text style={styles.pinText}>{i+1}</Text>
              </Pressable>
            ))}
          </View>
          <View style={styles.zoomControls}>
            <Pressable accessibilityLabel="Zoom avant" onPress={()=>setZoom(v=>clampZoom(v+0.25))} style={styles.zoomButton}><Text style={styles.zoomText}>＋</Text></Pressable>
            <Pressable accessibilityLabel="Zoom arrière" onPress={()=>{setZoom(v=>{const n=clampZoom(v-0.25);if(n===1)setOffset({x:0,y:0});return n;});}} style={styles.zoomButton}><Text style={styles.zoomText}>−</Text></Pressable>
            <Pressable accessibilityLabel="Recentrer la carte" onPress={()=>{setZoom(1);setOffset({x:0,y:0});}} style={styles.zoomButton}><Text style={styles.zoomText}>⌖</Text></Pressable>
          </View>
        </View>
        <Text style={styles.gestureHint}>Pince pour zoomer · Fais glisser pour déplacer · + / − pour régler le zoom</Text>
        <View style={styles.regionCard}>
          <View style={styles.regionTop}><Text style={styles.regionLabel}>{region.county}</Text><Text style={styles.regionNumber}>RÉGION {regions.findIndex(r=>r.id===selected)+1}/6</Text></View>
          <Text style={styles.regionTitle}>{region.name}</Text>
          <Text style={styles.regionDescription}>{region.description}</Text>
          <Link href="/map" style={styles.regionLink}>OUVRIR LE GUIDE DE LA RÉGION ↗</Link>
        </View>
        <View style={styles.regionChips}>
          {regions.map((r,i)=><Pressable key={r.id} onPress={()=>setSelected(r.id)} style={[styles.chip,selected===r.id&&styles.chipActive]}><Text style={[styles.chipText,selected===r.id&&styles.chipTextActive]}>{i+1}. {r.name}</Text></Pressable>)}
        </View>
        <Text style={styles.mapCredit}>Carte © Rockstar Games · Source cartographique : carte officielle de Leonida relayée par Leonida 6 Guide. Repères de région indicatifs.</Text>

        <View style={styles.sectionHeader}><Text style={styles.sectionTitle}>Ton guide de jeu</Text><Text style={styles.sectionSub}>Accès rapide aux autres rubriques</Text></View>
        <View style={styles.grid}>
          {sections.map(item=>(
            <Link key={item.href} href={item.href} asChild>
              <Pressable style={styles.card}>
                <Text style={styles.cardSymbol}>{item.symbol}</Text>
                <Text style={styles.cardTitle}>{item.title}</Text>
                <Text style={styles.cardDetail}>{item.detail}</Text>
                <Text style={styles.cardArrow}>OUVRIR ↗</Text>
              </Pressable>
            </Link>
          ))}
        </View>
        <Text style={styles.footer}>GTA 6 GUIDE RADAR · PROJET INDÉPENDANT, NON AFFILIÉ À ROCKSTAR GAMES</Text>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe:{flex:1,backgroundColor:"#100d18"},
  content:{padding:16,paddingBottom:44,maxWidth:900,width:"100%",alignSelf:"center"},
  header:{flexDirection:"row",alignItems:"center",justifyContent:"space-between",marginBottom:22,gap:10},
  kicker:{color:"#f58bc5",fontSize:9,letterSpacing:2,fontWeight:"900"},
  brand:{color:"#fff9f7",fontSize:21,fontWeight:"900",letterSpacing:1,marginTop:5},
  brandAccent:{color:"#ff83bd"},
  platformPill:{color:"#f2c8df",fontSize:9,fontWeight:"900",borderWidth:1,borderColor:"#78415f",borderRadius:20,paddingVertical:8,paddingHorizontal:10},
  mapHeading:{flexDirection:"row",justifyContent:"space-between",alignItems:"flex-end",gap:8},
  heroEyebrow:{color:"#ff9a32",fontSize:10,fontWeight:"900",letterSpacing:2},
  title:{color:"#fff9f7",fontSize:29,fontWeight:"900",marginTop:4},
  fullMap:{color:"#ff9acb",fontSize:10,fontWeight:"900",paddingBottom:5},
  mapIntro:{color:"#d0b9d0",fontSize:13,marginTop:7,marginBottom:13},
  mapShell:{alignSelf:"center",position:"relative",borderWidth:1,borderColor:"#8e5a82",borderRadius:14,overflow:"hidden",backgroundColor:"#142f2b"},
  mapCanvas:{position:"absolute",left:0,top:0,transformOrigin:"center"},
  mapImage:{width:"100%",height:"100%"},
  zoomControls:{position:"absolute",right:9,bottom:9,gap:6},
  zoomButton:{width:38,height:38,borderRadius:20,backgroundColor:"#261531",borderWidth:1,borderColor:"#f58bc5",alignItems:"center",justifyContent:"center"},
  zoomText:{color:"#fff9f7",fontSize:22,fontWeight:"900"},
  gestureHint:{color:"#b99eb9",fontSize:10,textAlign:"center",marginTop:6},
  pin:{position:"absolute",width:29,height:29,marginLeft:-14,marginTop:-14,borderRadius:18,borderWidth:2,borderColor:"#fff",backgroundColor:"#e85eaa",alignItems:"center",justifyContent:"center",elevation:5},
  pinActive:{backgroundColor:"#ff9a32",width:37,height:37,marginLeft:-18,marginTop:-18,borderColor:"#fff4d8"},
  pinText:{color:"#24102f",fontSize:11,fontWeight:"900"},
  regionCard:{backgroundColor:"#261531",borderWidth:1,borderColor:"#70405f",borderRadius:14,padding:15,marginTop:12},
  regionTop:{flexDirection:"row",justifyContent:"space-between",gap:8},
  regionLabel:{color:"#ffb0d0",fontSize:9,fontWeight:"900",letterSpacing:1},
  regionNumber:{color:"#d0b9d0",fontSize:9,fontWeight:"800"},
  regionTitle:{color:"#fff9f7",fontSize:22,fontWeight:"900",marginTop:7},
  regionDescription:{color:"#d0b9d0",fontSize:13,lineHeight:19,marginTop:5},
  regionLink:{color:"#ff9acb",fontSize:10,fontWeight:"900",marginTop:13},
  regionChips:{flexDirection:"row",flexWrap:"wrap",gap:7,marginTop:10},
  chip:{borderWidth:1,borderColor:"#55345f",borderRadius:20,paddingVertical:8,paddingHorizontal:10,backgroundColor:"#1c1227"},
  chipActive:{backgroundColor:"#542344",borderColor:"#f58bc5"},
  chipText:{color:"#d0b9d0",fontSize:10,fontWeight:"800"},
  chipTextActive:{color:"#fff4f8"},
  mapCredit:{color:"#967d98",fontSize:9,lineHeight:14,marginTop:10},
  sectionHeader:{marginTop:28,marginBottom:12},
  sectionTitle:{color:"#fff9f7",fontSize:20,fontWeight:"900"},
  sectionSub:{color:"#cbb6ce",fontSize:12,marginTop:3},
  grid:{flexDirection:"row",flexWrap:"wrap",gap:10,justifyContent:"space-between"},
  card:{width:"48%",minWidth:145,flexGrow:1,flexBasis:"46%",backgroundColor:"#211829",borderColor:"#4b344f",borderWidth:1,borderRadius:13,padding:14,minHeight:112,justifyContent:"flex-start"},
  cardSymbol:{color:"#ff83bd",fontSize:22,marginBottom:9},
  cardTitle:{color:"#fff9f7",fontSize:14,fontWeight:"900"},
  cardDetail:{color:"#d0b9d0",fontSize:11,lineHeight:16,marginTop:5},
  cardArrow:{color:"#ff83bd",fontSize:9,fontWeight:"900",letterSpacing:1,marginTop:11},
  footer:{color:"#9e809b",fontSize:9,letterSpacing:.5,marginTop:26,textAlign:"center"}
});
