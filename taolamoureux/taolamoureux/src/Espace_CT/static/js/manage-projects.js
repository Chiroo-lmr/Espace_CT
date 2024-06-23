var manageProjectsButton = document.getElementById('buttonManageProjects')
var nvCarteProject = document.getElementById('nvCarteProject')
var editing_buttons = document.getElementsByClassName("editing_buttons")
var buttonAddProjects = document.getElementById('buttonAddProjects')
var dbuttonAddProjects = document.getElementById('dbuttonAddProjects')
var dbuttonAddProjectsIdeas = document.getElementById('dbuttonAddProjectsIdeas')
var nvCarteProjectIdea = document.getElementById('nvCarteProjectIdea')
var editing = false


manageProjectsButton.innerHTML = "Gérer les projets"
dbuttonAddProjects.style.display = "none"
dbuttonAddProjectsIdeas.style.display = "none"

manageProjectsButton.addEventListener('click', function() {
    if (editing == false){
        manageProjectsButton.innerHTML = "Revenir à la vue statique"
        for (let i = 0; i < editing_buttons.length; i++) {
            editing_buttons[i].style.display = "flex"
        }
        dbuttonAddProjectsIdeas.style.display = "flex"
        dbuttonAddProjects.style.display = "flex"
        editing = true
    } else {
        nvCarteProject.style.display = "none"
        manageProjectsButton.innerHTML = "Gérer les projets"
        for (let i = 0; i < editing_buttons.length; i++) {
            editing_buttons[i].style.display = "none"
        }
        dbuttonAddProjectsIdeas.style.display = "none"
        dbuttonAddProjects.style.display = "none"
        editing = false
    }
});
buttonAddProjects.addEventListener('click', function() {
    dbuttonAddProjects.style.display = "none"
    nvCarteProject.style.display = "flex"
});
dbuttonAddProjectsIdeas.addEventListener('click', () => {
    dbuttonAddProjectsIdeas.style.display = "none"
    nvCarteProjectIdea.style.display = "flex"
});