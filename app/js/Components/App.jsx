import React from "react";
import { Route, NavLink, Redirect, Router } from "react-router-dom";
import { Button, Glyphicon } from "react-bootstrap";
import { Provider } from "mobx-react";
import injectStyles from "react-jss";
import { isFunction } from "lodash";
import { createBrowserHistory } from "history";

// Views
// import PersonList from "./PersonList";
import PersonQuery from "./PersonQuery";
import PersonDetails from "./PersonDetails";
import WhatsNew from "./WhatsNew";

import CustomPrompt from "./CustomPrompt";

// Singletons
import PersonTypes from "../Stores/PersonTypes";

// Stores
import PersonStore from "../Stores/Persons";

const history = createBrowserHistory({
  getUserConfirmation: CustomPrompt
});

const singletons = {
  personTypes: new PersonTypes()
};

const stores = {
  personStore: new PersonStore()
};

for (const key in stores) {
  let store = stores[key];
  if (store.registerHistory && typeof store.registerHistory === "function") {
    store.registerHistory(history); // Make the history available in each store
  }
}

const NotFound = () => <h1>This page does not exist</h1>;

const navStyles = {
  container: {
    display: "grid",
    gridTemplateRows: "160px 1fr",
    height: "100vh",
    "& .glyphicon":{
      marginRight:"8px",
    },
    "& h1":{
      fontSize:"1.80em",
      color:"#1ca8dd",
    },
    "& h2":{
      fontSize:"1.25em",
      fontStyle:"italic",
      "& .glyphicon":{
        marginRight:"2px",
        fontSize:"0.9em"
      }
    },
    "& h3":{
      fontSize:"1.1em"
    },
    "& hr":{
      opacity:"0.25"
    },
    "& ul":{
      listStyle:"none",
      paddingLeft:"0",
      marginLeft:"16px",
    },
    "& .nav-container .navlink":{
      display: "none",
    },
    "& .nav-container.active .navlink": {
      display: "block",
    },
    "& .nav-container": {
      whiteSpace: "nowrap"
    },
    "& .nav-container:hover .nav-header::after, & .nav-container.active .nav-header::after": {
      content: "'+'",
      fontStyle: "normal",
      fontWeight: "bold",
      position: "absolute",
      left: "16px",
    },
    "& a":{
      color:"white",
      opacity:0.60,
      fontWeight:"300",
      "&.active":{
        opacity:1,
        fontWeight:"normal"
      }
    },
    "& .contact":{
      color:"#ffbdbd",
    },
    "@media screen and (max-width:1024px)":{
      textAlign:"center",
      fontSize:"1.2em",
      "& h1":{
        fontSize:"1.5em",
        marginLeft:"-20px"
      },
      "& ul":{
        lineHeight:"1.6",
        fontSize:"1.3em",
      }
    }
  },
  plusIcon:{
    position:"absolute",
    top:"0",
    left:"0",
    width:"240px"
  },
  plusText:{
    fontSize:"12pt",
    fontFamily:"Fredoka One",
    fill:"white"
  },
  logolink:{
    fontSize:"1.5em",
    fontStyle:"italic",
    verticalAlign:"middle",
    color:"white",
    opacity:"1",
    fontWeight:"bold"
  },
  menuItem:{
    fontSize:"1.5em",
    textDecoration:"none !important"
  },
  navigationList:{
    padding: "0px 20px 20px 20px",
    cursor: "pointer"
  }
};

@injectStyles(navStyles)
class Navigation extends React.Component {
  constructor(props) {
    super(props);
    const { location : { pathname } } = this.props.history;
  }

  render() {
    let { classes } = this.props;
    return (
      <div className={classes.container}>
        <div>
          <Glyphicon glyph="asterisk" style={{color: "blue", fontSize: "72pt", padding: "8px", position: "relative"}}/><span style={{color: "gold", fontSize: "36pt", marginLeft: "-60px", marginTop: "0px", zIndex: "1", position: "relative"}}>Demo</span>
        </div>
        <div className={classes.navigationList}>
          <div className={classes.menuItem}><a style={{color: "gold"}} href='/whatsnew'>What&apos;s New?</a></div>
          <h1>Outreach</h1>
          <ul>
            {/*
            */}
            <li>
              <h2 className={"nav-header"}><Glyphicon glyph="book"/> Persons</h2>
              <ul>
                <li><NavLink className={"navlink"} exact={true} activeClassName="active" to="/person"><Glyphicon glyph="search"/>Find persons</NavLink></li>
                <li><NavLink className={"navlink"} exact={true} activeClassName="active" to="/person/new"><Glyphicon glyph="plus"/>Add a new person</NavLink></li>
              </ul>
            </li>
          </ul>
          <h1>Planning</h1>
          <ul>
          </ul>
          <br/>
          <div className={classes.menuItem}><a href='mailto:simon.bell@epfl.ch?subject=APP: ' className={"contact"}>Contact Us...</a></div>
        </div>
      </div>
    );
  }
}

let styles = {
  "@global body":{
    "font-family": "'Lato', sans-serif"
  },
  container:{
    display:"grid",
    width:"100vw",
    height:"100vh",
    overflow:"hidden",
    gridTemplateColumns: "250px 1fr",
    gridTemplateAreas: "'sidebar body'",
    "@media screen and (max-width:1024px)":{
      gridTemplateColumns: "1fr",
      gridTemplateRows: "auto auto",
      gridTemplateAreas: "'sidebar' 'body'",
    }
  },
  body:{
    gridArea: "body",
    height:"100vh",
    overflow:"auto",
    padding: "0",
    "& hr":{
      borderTop: "1px solid #cacaca"
    },
    "@media screen and (max-width:1024px)":{
      height:"calc(100vh - 90px)",
      fontSize:"1.2em"
    },
    "& h3":{
      marginBottom: "20px"
    }
  },
  sidebar:{
    position:"relative",
    gridArea: "sidebar",
    height:"100vh",
    // overflow:"auto",
    color:"white",
    transition:"height 0.5s ease",
    "@media screen and (max-width:1024px)":{
      overflow:"hidden",
      height:"90px"
    }
  },
  mobileMenuButton:{
    position:"absolute",
    top:"25px",
    right:"30px",
    display:"none",
    border:"1px solid #ecf0f1",
    color:"#ecf0f1",
    "@media screen and (max-width:1024px)":{
      display:"block"
    },
    "&:active:hover, &:active, &:hover, &:focus":{
      border:"1px solid #ecf0f1",
      color:"#ecf0f1",
    }
  },
  "@media screen and (max-width:1024px)":{
    "@global body":{
      overflow:"hidden"
    }
  },
  menuExpanded:{
    "& $sidebar":{
      height:"100vh",
      overflow:"auto",
    }
  }
};

@injectStyles(styles)
class _App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {menuExpanded: false};
  }

  expandSidebar() {
    this.setState({menuExpanded: !this.state.menuExpanded});
  }

  async componentDidMount(){
    document.addEventListener("click", (e) => {
      if(isFunction(e.target.className.match) && e.target.className.match(/navlink/gi)){
        this.setState({menuExpanded: false});
        document.querySelector("#contentNav").scrollTo(0, 0);
      }
    });
  }

  render() {
    let {classes} = this.props;
    return (
      <Provider {...stores}>
        <Router history={history}>
          <div className={[classes.container, this.state.menuExpanded? classes.menuExpanded: ""].join(" ")}>
            <div className={classes.sidebar} id="contentNav">
              <Navigation history={history} />
              <Button className={classes.mobileMenuButton} onClick={this.expandSidebar.bind(this)}><Glyphicon glyph="menu-hamburger"/></Button>
            </div>
            <div className={classes.body}>
              <Route exact path="/" component={WhatsNew} />
              <Route exact path="/whatsnew" component={WhatsNew} />
              {/*
              */}
              <Route exact path="/person" component={PersonQuery} />
              <Route exact path="/person/:id" component={PersonDetails} />
              <Route exact path="/not-found" component={NotFound} />
            </div>
          </div>
        </Router>
      </Provider>
    );
  }
}

const App = () => (
  <_App />
);
export default App;

