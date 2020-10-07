$(document).ready(function () {
  // Calculate the proficiency bonus based on level.
  let profBonus = parseInt($("#level").text());
  console.log(Math.ceil(profBonus / 4));
  $("#prof").text("Proficiency bonus: " + Math.ceil(profBonus / 4));
  // Calculate modifiers based on other attributes and add contextual clues for the user.
  $(".base").each(function () {
    let idString = $(this).attr("id");
    let realStat = $(this).text();
    let modStat = Math.floor((parseInt(realStat) - 10) / 2);

    if (modStat > 0) {
      $("#" + idString + "-mod").text("+" + modStat);
    } else if (modStat < 0) {
      $("#" + idString + "-mod").text(modStat);
    } else {
      $("#" + idString + "-mod").text(modStat);
    }
  });
  // Mark which saving-throws add the proficiency bonus.
  $(".saving-throw").each(function () {
    if ($(this).hasClass("True") == true) {
      $(this).html('<i class="fas fa-check"></i>');
    } else {
      return;
    }
  });
  // Essentially the same, marking which skills have been selected as proficient.
  $(".skill-list").each(function () {
    if ($(this).hasClass("True") == true) {
      $(this).html('<i class="fas fa-check"></i>');
    } else {
      return;
    }
  });
  // The bread and butter of the script, here we perform the actual dice-roll functions.
  $(".dice-roller").click(function () {
    // d20 is a randomized integer between 1 and 20.
    let d20 = Math.floor(Math.random() * 20) + 1;
    if ($(this).hasClass("skill-list-dice") == true) {
      $("#dieModalTitle").empty();
      $("#dieModalTitle").html("Skill check: ");
      $("#diceOutPut").empty();
      $("#diceOutPut").html(d20);
    } else if ($(this).hasClass("saving-throw-dice") == true) {
      $("#dieModalTitle").empty();
      $("#dieModalTitle").html("Saving throw: ");
      $("#diceOutPut").empty();
      $("#diceOutPut").html(d20);
    } else if ($(this).hasClass("attribute-roll") == true) {
      $("#dieModalTitle").empty();
      $("#dieModalTitle").html("Attribute check: ");
      $("#diceOutPut").empty();
      $("#diceOutPut").html(d20);
    } else {
      $("#dieModalTitle").empty();
      $("#dieModalTitle").html("Unspecified roll: ");
      $("#diceOutPut").empty();
      $("#diceOutPut").html(d20);
    }
  });
});
