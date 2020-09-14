<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.4" tiledversion="2020.08.05" name="dungeon" tilewidth="32" tileheight="32" tilecount="272" columns="16">
 <image source="../sprites/Arena Tileset.png" width="512" height="544"/>
 <terraintypes>
  <terrain name="Neues Terrain" tile="86"/>
  <terrain name="Neues Terrain" tile="17"/>
  <terrain name="Neues Terrain" tile="26"/>
 </terraintypes>
 <tile id="0" terrain=",,,1"/>
 <tile id="1" terrain=",,1,1"/>
 <tile id="2" terrain=",,1,"/>
 <tile id="8" terrain=",,,2"/>
 <tile id="9" terrain=",,2,2"/>
 <tile id="10" terrain=",,2,"/>
 <tile id="16" terrain=",1,,1"/>
 <tile id="17" terrain="1,1,1,1"/>
 <tile id="18" terrain="1,,1,"/>
 <tile id="24" terrain=",2,,2"/>
 <tile id="25" terrain="2,2,2,2"/>
 <tile id="26" terrain="2,,2,"/>
 <tile id="32" terrain=",1,,"/>
 <tile id="33" terrain="1,1,,"/>
 <tile id="34" terrain="1,,,"/>
 <tile id="69" terrain=",,,0"/>
 <tile id="70" terrain=",,0,0"/>
 <tile id="71" terrain=",,0,">
  <objectgroup draworder="index" id="2">
   <object id="1" x="0" y="0" width="13.1845" height="31.8979"/>
  </objectgroup>
 </tile>
 <tile id="85" terrain=",0,,0"/>
 <tile id="86" terrain="0,0,0,0"/>
 <tile id="87" terrain="0,,0,">
  <objectgroup draworder="index" id="2">
   <object id="1" type="fvsv" x="0.0850611" y="-0.0850611" width="12.9293" height="31.983"/>
  </objectgroup>
 </tile>
 <tile id="101" terrain=",0,,"/>
 <tile id="102" terrain="0,0,,">
  <objectgroup draworder="index" id="2">
   <object id="1" x="0.0850611" y="2.44249e-15" width="31.983" height="26.0287"/>
   <object id="2" x="16.8421" y="24.7528">
    <point/>
   </object>
  </objectgroup>
 </tile>
 <tile id="103" terrain="0,,,"/>
 <tile id="140">
  <objectgroup draworder="index" id="2">
   <object id="1" x="0" y="0" width="32" height="32"/>
  </objectgroup>
 </tile>
 <wangsets>
  <wangset name="Neues Wang-Set" tile="-1">
   <wangedgecolor name="" color="#ff0000" tile="-1" probability="1"/>
   <wangedgecolor name="" color="#00ff00" tile="-1" probability="1"/>
   <wangcornercolor name="" color="#ff0000" tile="-1" probability="1"/>
   <wangcornercolor name="" color="#00ff00" tile="-1" probability="1"/>
   <wangtile tileid="70" wangid="0x12222211"/>
   <wangtile tileid="86" wangid="0x22222222"/>
   <wangtile tileid="102" wangid="0x22111222"/>
   <wangtile tileid="128" wangid="0x11111111"/>
   <wangtile tileid="129" wangid="0x11111111"/>
   <wangtile tileid="130" wangid="0x11111111"/>
   <wangtile tileid="131" wangid="0x11111111"/>
   <wangtile tileid="132" wangid="0x11111111"/>
   <wangtile tileid="133" wangid="0x11111111"/>
   <wangtile tileid="134" wangid="0x11111111"/>
   <wangtile tileid="135" wangid="0x11111111"/>
   <wangtile tileid="136" wangid="0x11111111"/>
   <wangtile tileid="138" wangid="0x11112221"/>
   <wangtile tileid="139" wangid="0x22211111"/>
   <wangtile tileid="141" wangid="0x11112221"/>
   <wangtile tileid="142" wangid="0x22211111"/>
   <wangtile tileid="144" wangid="0x11111111"/>
   <wangtile tileid="145" wangid="0x11111111"/>
   <wangtile tileid="146" wangid="0x11111111"/>
   <wangtile tileid="147" wangid="0x11111111"/>
   <wangtile tileid="148" wangid="0x11111111"/>
   <wangtile tileid="149" wangid="0x11111111"/>
   <wangtile tileid="150" wangid="0x11111111"/>
   <wangtile tileid="151" wangid="0x11111111"/>
   <wangtile tileid="152" wangid="0x11111111"/>
  </wangset>
 </wangsets>
</tileset>
