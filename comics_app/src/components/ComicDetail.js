import React from 'react';
import {Image, View, Modal, StyleSheet} from 'react-native';
import ImageViewer from 'react-native-image-zoom-viewer';



export default class ComicDetail extends React.Component{
    
    constructor(){
        super();
        this.state = {
            dataSource: [],
            isModalVisible: false,
            isReady: false
        }
    }

    onEnter = () =>{
        fetch("https://f5fd296b.ngrok.io/comics/"+this.props.objectId+"/", {
            method: "GET"
        }).then((response) => response.json()).then((responseJson) => {
            if(responseJson){
                this.setState({dataSource: responseJson});
            }
        });
    }

    ShowModal(visible){
        this.setState({isModalVisible: false});
    }

    render(){
        const urls = [{url: this.props.image},];
        return (
            <View style={styles.MainContainer}>
                <ImageViewer style={styles.imageThumbnail} imageUrls={urls} onRequestClose={() => this.ShowModal()} backgroundColor="white"/>
            </View>
        )
    }
}




const styles = StyleSheet.create({
    MainContainer: {
      justifyContent: 'center',
      flex: 1,
      //paddingTop: 30,
      margin:10,
      borderColor: "red",
      borderWidth: 1
    },
    imageThumbnail: {
      justifyContent: 'center',
      alignItems: 'center',
      resizeMode: 'cover',
      width:500,
      height: 250
    },
  });