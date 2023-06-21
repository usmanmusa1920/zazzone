function showCustomZoneNameField(){
    document.querySelector('.zone_custom').style.display = 'block'
    document.querySelector('.zone_span').style.display = 'none'
    document.querySelector('.zone_custom').innerHTML= '<input type="text" name="custom_zone_type" placeholder="What is your zone type e.g school zone, public zone, etc" required>'
}


function hideCustomZoneNameField(){
    document.querySelector('.zone_custom').style.display = 'none'
    document.querySelector('.zone_span').style.display = 'block'
}
