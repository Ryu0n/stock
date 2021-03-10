import ListStockMarket from './components/inquiry/list/listStockMarket';
import './App.css';
import React, { Component } from 'react';


class App extends Component{

  state = {
    view_mode: 'market_list',
  }

  constructor(props){
    super(props);
  }

  // shouldComponentUpdate(){
  // }
  
  render(){
    let template = null;
    if (this.state.view_mode == 'market_list') {
        // template = <ListStockMarket onChangeState={this.setViewMode().bind(this)}/>;
        template = <ListStockMarket onChangeState={function(){
          this.setState(
            {view_mode : 'item_list'}
          );
        }.bind(this)
      }
      />;
    }
    else if (this.state.view_mode == 'item_list') {
      
    }

    return (
      <div className="App">
        {template}
      </div>
    );
  }

  // 해당 메소드를 static 하게 정의해야함. (방법 찾아보기)
  // setViewMode(){
  //   this.setState(
  //     { view_mode : 'item_list' }
  //   )
  // }
}

export default App;
