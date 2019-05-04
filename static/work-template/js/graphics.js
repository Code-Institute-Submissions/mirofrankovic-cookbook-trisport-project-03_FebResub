function designGraphs(error, recipeData){
    var ndx = crossfilter(recipeData);
    console.log(recipeData);
    show_meal_type_graph(ndx);
    show_sport_type_graph(ndx);
    show_race_day_graph(ndx);
    show_vegan_meal_graph(ndx);
    
    dc.renderAll();
}

function show_meal_type_graph(ndx){
    var meal_typeSun = ndx.dimension(dc.pluck("meal_type"));
    var meal_typeGar = meal_typeSun.group();
    
    dc.barChart("#meal_type-graph")
       .width(350)
       .height(250)
       .margins({top: 20, right: 20, bottom: 30, left: 10})
       .dimension(meal_typeSun)
       .group(meal_typeGar)
       .transitionDuration(500)
       .x(d3.scale.ordinal())
       .xUnits(dc.units.ordinal)
       .elasticY(true)
       .xAxisLabel("Meal-Type")
       .yAxis().tickFormat(d3.format("d"));
    
    
    
}