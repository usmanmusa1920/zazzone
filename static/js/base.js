// the below two functions are for large screen size
function showMenu(){
  // pop class attribute
  document.querySelector('.pop').style.position = 'fixed'
  document.querySelector('.pop').style.width = '40%'
  document.querySelector('.pop').style.backgroundColor = 'lightgrey'
  document.querySelector('.pop').style.display = 'flex'
  document.querySelector('.pop').style.paddingTop = '3px'
  document.querySelector('.pop').style.alignItems = 'center'
  document.querySelector('.pop').style.flexDirection = 'column'
  document.querySelector('.pop').style.border = 'solid 3px grey'
  document.querySelector('.pop').style.borderRadius = '7px'
  // end pop class attribute

  // pop_mid_board classattribute
  document.querySelector('.pop_mid_board').style.width = '80%'
  document.querySelector('.pop_mid_board').style.maxHeight = '140px'
  document.querySelector('.pop_mid_board').style.overflow = 'auto'
  document.querySelector('.pop_mid_board').style.display = 'flex'
  document.querySelector('.pop_mid_board').style.flexDirection = 'column'
  document.querySelector('#mid_linkSm').style.display = 'none'
  // end pop_mid_board class attribute

  // these are buttons that wil send the events
  // for showMenu
  document.querySelector('#show_menu').style.display = 'none'
  // for hideMenu
  document.querySelector('#hide_menu').style.display = 'flex'
  document.querySelector('#hide_menu').style.flexDirection = 'flex-end'
  document.querySelector('#hide_menu').style.border = 'none'
  document.querySelector('#hide_menu').style.backgroundColor = 'transparent'
}

function hideMenu(){
  // This will hide the pop-up div
  document.querySelector('.pop').style.display = 'none'
  // these are buttons that wil send the events
  // for hideMenu
  document.querySelector('#hide_menu').style.display = 'none'
  // for showMenu
  document.querySelector('#show_menu').style.display = 'flex'
  document.querySelector('#show_menu').style.flexDirection = 'flex-end'
}







// the following two functions are for small screen size
function showMenuSm(){
  // pop class attribute
  document.querySelector('.pop').style.position = 'fixed'
  if (window.innerWidth < 701){
    document.querySelector('.pop').style.width = '90%'
    }
  else{
    document.querySelector('.pop').style.width = '80%'
  }
  document.querySelector('.pop').style.backgroundColor = 'lightgrey'
  document.querySelector('.pop').style.display = 'flex'
  document.querySelector('.pop').style.paddingTop = '3px'
  document.querySelector('.pop').style.alignItems = 'center'
  document.querySelector('.pop').style.flexDirection = 'column'
  document.querySelector('.pop').style.border = 'solid 3px grey'
  document.querySelector('.pop').style.borderRadius = '7px'
  // end pop class attribute

  // pop_mid_board classattribute
  document.querySelector('.pop_mid_board').style.width = '80%'
  document.querySelector('.pop_mid_board').style.maxHeight = '140px'
  document.querySelector('.pop_mid_board').style.overflow = 'auto'
  document.querySelector('.pop_mid_board').style.display = 'flex'
  document.querySelector('.pop_mid_board').style.flexDirection = 'column'
  // end pop_mid_board class attribute

  // these are buttons that wil send the events
  // for showMenu
  document.querySelector('#show_menu_sm').style.display = 'none'
  // for hideMenu
  document.querySelector('#hide_menu_sm').style.display = 'flex'
  document.querySelector('#hide_menu_sm').style.flexDirection = 'flex-end'
  document.querySelector('#hide_menu_sm').style.border = 'none'
  document.querySelector('#hide_menu_sm').style.backgroundColor = 'transparent'
}

function hideMenuSm(){
  // This will hide the pop-up div
  document.querySelector('.pop').style.display = 'none'

  
  // these are buttons that wil send the events
  // for hideMenu
  document.querySelector('#hide_menu_sm').style.display = 'none'
  // for showMenu
  document.querySelector('#show_menu_sm').style.display = 'flex'
  document.querySelector('#show_menu_sm').style.flexDirection = 'flex-end'
}

// These two functions below are just for more links of a post
function showDetail(){
  document.querySelector('.detail_popup').style.display = 'flex'
  document.querySelector('.detail_popup').style.justifyContent = 'space-between'
  document.querySelector('.detail_popup').style.width = '30%'
  document.querySelector('.detail_popup').style.backgroundColor = 'whitesmoke'
  document.querySelector('.detail_popup').style.border = 'solid 3px gray'
  document.querySelector('.detail_popup').style.borderRadius = '5px'
  document.querySelector('.detail_popup').style.position = 'fixed'
  document.querySelector('.detail_popup').style.paddingLeft = '10px'
  document.querySelector('.detail_popup').style.paddingRight = '10px'
  document.querySelector('.detail_popup').style.paddingBottom = '5px'
  document.querySelector('.detail_popup').style.paddingTop = '5px'


  document.querySelector('.detail_div').style.display = 'flex'
  document.querySelector('.detail_div').style.flexDirection = 'column'
  
  
  document.querySelector('#show_detail_btn').style.display = 'none'
  document.querySelector('#hide_detail_btn').style.display = 'block'
}

function hideDetail(){
  document.querySelector('.detail_popup').style.display = 'none'
  document.querySelector('#hide_detail_btn').style.display = 'none'
  document.querySelector('#show_detail_btn').style.display = 'block'
}
// end of two detail function