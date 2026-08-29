
//CHOOSE A CASE
function choose_a_case(){
	var case_disease_id = document.getElementById("select_1").value; 
	alert("CASE DISEASE ID IS: " + case_disease_id);
	
	var drug_name = document.getElementById("select_2");
	var length1 = drug_name.options.length;
	alert("length1 = " + length1);
	
	
	/*alert(typeof case_disease_id);
	alert(typeof drug_name.options[1].value);*/


	for (i=0; i<length1; i++)
		{
			var x = parseInt(drug_name.options[i].value);
			var y = parseInt(case_disease_id);
			if( x!= y)
			{
				drug_name.remove(i);
				/*alert("deleted");*/
			}
		}
	
	alert("HERE");
	var length2 = drug_name.options.length;
	lert("length2 = " + length2);
}
