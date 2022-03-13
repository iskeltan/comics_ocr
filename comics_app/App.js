import React from 'react';
import { StyleSheet, Text, View } from 'react-native';
import Home from './src/components/Home';
import ComicDetail from './src/components/ComicDetail';
import {Router, Stack, Scene} from 'react-native-router-flux'

export default function App() {
  return (
    <Router>
      <Stack key="root" >
        <Scene key="Search" component={Home} title="Home" initial={true} navigationBarStyle={{height: 30}} hideNavBar={true} />
        <Scene key="Detail" component={ComicDetail} title="Detail" />
      </Stack>
    </Router>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#393e42',
    alignItems: 'center',
    justifyContent: 'center',
  },
});


