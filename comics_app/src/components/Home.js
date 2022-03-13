import React from 'react';
import {Text, View, Image, FlatList, RefreshControl} from 'react-native';
import { Searchbar } from 'react-native-paper';
import {StyleSheet, TouchableHighlight} from 'react-native';
import { Actions } from 'react-native-router-flux';

export default class Home extends React.Component{

    constructor() {
        super();
        this.state = {
          dataSource: [],
          isRefreshing: false
        };
      }

      onRefresh(){
          this.setState({isRefreshing: true});
          this.setState({dataSource: []});
        fetch("https://f5fd296b.ngrok.io/comics/random/", {
            method: "GET"
        }).then((response) => response.json()).then((responseJson) => {
            if(responseJson){
                this.setState({dataSource: responseJson});
            }
        });
        this.setState({isRefreshing: false});
      }

      componentDidMount = () => {
        this.onRefresh();
    }

    onSearch = query => {
        if(query.length >= 2){
            this.setState({isRefreshing: true});
            this.setState({dataSource: []});
            let requestURL = "http://localhost:8000/comics/search/?q="+query;
            fetch(requestURL, {
                method: "GET"
            }).then((response) => response.json()).then((responseJson) => {
                if(responseJson){
                    let responseData = []
                    responseJson.map((item, key) => responseData.push({id: item.id, image: "http://localhost:8000" + item.image}));
                    this.setState({dataSource: responseData});
                }else{
                    this.setState({dataSource: []});
                }
            }).then(
                () => {
                    this.setState({isRefreshing: false});
                }
            );
        }else{
            this.onRefresh()
        }
    }


    goDetail = (objectId, imageUrl) => {
        Actions.Detail({objectId: objectId, image: imageUrl});
    }

    render(){
        return (
        <View style={{flex: 1}}>
            <Searchbar placeholder="Ara" style={{marginTop: 10}} onChangeText={this.onSearch.bind(this)} />
            <View style={styles.MainContainer}>
        <FlatList
          refreshControl={
              <RefreshControl refreshing={this.state.isRefreshing} onRefresh={this.onRefresh.bind(this)} />
          }
          data={this.state.dataSource}
          renderItem={({ item }) => (
            <TouchableHighlight style={{ flex: 1, flexDirection: 'column', margin: 2 }} onPress={this.goDetail.bind(this, item.id, item.image)}>
              <Image style={styles.imageThumbnail} source={{ uri: item.image }} />
            </TouchableHighlight>
          )}
          //Setting the number of column
          numColumns={2}
          keyExtractor={(item, index) => index.toString()}
          style={{backgroundColor: '#e1e1e1'}}
        />
      </View>
        </View>
        )
    }
}

const styles = StyleSheet.create({
    MainContainer: {
      justifyContent: 'center',
      flex: 1,
      //paddingTop: 30,
    },
    imageThumbnail: {
      justifyContent: 'center',
      alignItems: 'center',
      height: 100,
    },
  });