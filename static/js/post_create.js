function showSnippetField(){
  document.querySelector('.code').style.display = 'block';

  // Styling the div that will hide snippet field
  document.querySelector('.hide_code_field').style.display = 'block';
  document.querySelector('.hide_code_field').style.marginTop = '5px';
  document.querySelector('.hide_code_field').style.borderRadius = '3px';
  // document.querySelector('.hide_code_field').style.width = 'fitContent';
  document.querySelector('.hide_code_field').style.background = 'grey';
  document.querySelector('.hide_code_field').style.color = 'white';
  document.querySelector('.hide_code_field').style.padding = '3px';
  // End of hidingdiv

  document.querySelector('.show_code_field').style.display = 'none';
}

function hideSnippetField(){
  document.querySelector('.code').style.display = 'none';
  document.querySelector('.hide_code_field').style.display = 'none';
  document.querySelector('.show_code_field').style.display = 'block';
}