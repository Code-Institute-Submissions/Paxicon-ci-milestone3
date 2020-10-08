// This script is called exclusively by char_profile.html and provides functionaltiy for the character-sheet.

$(document).ready(function () {
  let root_url = location.href;
  // A small call to the API, to get a JSON copy of the database-object representing the character-sheet.
  $.post(root_url, function (data) {
    // Calculate the proficiency bonus based on level.
    let level = data.ClassObj.Lvl;
    let profBonus = parseInt(Math.ceil(level / 4));

    $("#prof").text("Proficiency bonus: " + profBonus);
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
      // The Results var stores the result of all rolls, so they can then be passed to the
      // modal.
      let results = [];
      // This arrow-function is used later to get a sum total of a roll
      const addResults = (a, b) => a + b;

      // This function checks the particular dice-roller clicked for the attribute-modifier that governs it, by checking for the appropriate CSS-class on the roller itself.
      function getMod(thisObj) {
        if (thisObj.hasClass("str-mod")) {
          let modVal = parseInt(
            Math.floor((data.AttributeList.strength - 10) / 2)
          );
          return modVal;
        } else if (thisObj.hasClass("dex-mod")) {
          let modVal = parseInt(
            Math.floor((data.AttributeList.dexterity - 10) / 2)
          );
          return modVal;
        } else if (thisObj.hasClass("con-mod")) {
          let modVal = parseInt(
            Math.floor((data.AttributeList.constitution - 10) / 2)
          );
          return modVal;
        } else if (thisObj.hasClass("int-mod")) {
          let modVal = parseInt(
            Math.floor((data.AttributeList.intelligence - 10) / 2)
          );
          return modVal;
        } else if (thisObj.hasClass("wis-mod")) {
          let modVal = parseInt(
            Math.floor((data.AttributeList.wisdom - 10) / 2)
          );
          return modVal;
        } else if (thisObj.hasClass("cha-mod")) {
          let modVal = parseInt(
            Math.floor((data.AttributeList.charisma - 10) / 2)
          );
          return modVal;
        }
      }

      if ($(this).hasClass("skill-list-dice") == true) {
        // Empties container of results from last call.
        $("#dieModalTitle").empty();
        $("#diceOutPut").empty();
        // Handler to add the proficiency bonus to proficient rolls.
        if ($(this).hasClass("True") == true) {
          results.push(d20);
          results.push(getMod($(this)));
          results.push(profBonus);
          $("#dieModalTitle").html("Skill check (Proficient): ");
          $("#diceOutPut").empty();
          $("#diceOutPut").html(
            "<ul class='list-group'><li class='list-group-item'>Roll: " +
              results[0] +
              "</li> <li class='list-group-item'>Attribute bonus: " +
              results[1] +
              "</li> <li class='list-group-item'>Proficiency bonus: " +
              results[2] +
              "</li><li class='list-group-item'><br><h4>Result: " +
              results.reduce(addResults) +
              "</h4></li></ul>"
          );
        } else {
          results.push(d20);
          results.push(getMod($(this)));
          $("#dieModalTitle").html("Skill check: ");

          $("#diceOutPut").empty();
          $("#diceOutPut").html(
            "<ul class='list-group'><li class='list-group-item'>Roll: " +
              results[0] +
              "</li> <li class='list-group-item'>Attribute bonus: " +
              results[1] +
              "</li><li class='list-group-item'><br><h4>Result: " +
              results.reduce(addResults) +
              "</h4></li></ul>"
          );
        }
      } else if ($(this).hasClass("saving-throw-dice") == true) {
        // Empties container of results from last call.
        $("#dieModalTitle").empty();
        $("#diceOutPut").empty();
        // Handler to add the proficiency bonus to proficient rolls.
        if ($(this).hasClass("True") == true) {
          results.push(d20);
          results.push(getMod($(this)));
          results.push(profBonus);
          $("#dieModalTitle").html("Saving throw (Proficient): ");
          $("#diceOutPut").empty();
          $("#diceOutPut").html(
            "<ul class='list-group'><li class='list-group-item'>Roll: " +
              results[0] +
              "</li> <li class='list-group-item'>Attribute bonus: " +
              results[1] +
              "</li> <li class='list-group-item'>Proficiency bonus: " +
              results[2] +
              "</li><li class='list-group-item'><br><h4>Result: " +
              results.reduce(addResults) +
              "</h4></li></ul>"
          );
        } else {
          results.push(d20);
          results.push(getMod($(this)));
          $("#dieModalTitle").html("Saving throw: ");

          $("#diceOutPut").empty();
          $("#diceOutPut").html(
            "<ul class='list-group'><li class='list-group-item'>Roll: " +
              results[0] +
              "</li> <li class='list-group-item'>Attribute bonus: " +
              results[1] +
              "</li><li class='list-group-item'><br><h4>Result: " +
              results.reduce(addResults) +
              "</h4></li></ul>"
          );
        }
      } else if ($(this).hasClass("attribute-roll") == true) {
        results.push(d20);
        results.push(getMod($(this)));
        $("#dieModalTitle").html("Attribute check: ");
        $("#diceOutPut").html(
          "<ul class='list-group'><li class='list-group-item'>Roll: " +
            results[0] +
            "</li> <li class='list-group-item'>Attribute bonus: " +
            results[1] +
            "</li><li class='list-group-item'><br><h4>Result: " +
            results.reduce(addResults) +
            "</h4></li></ul>"
        );
      } else {
        $("#dieModalTitle").html("Unspecified roll: ");

        $("#diceOutPut").html(d20);
      }
    });
  });
});
