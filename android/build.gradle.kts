// Use 'layout.buildDirectory.value' for the initial assignment
val newBuildDir: Directory = rootProject.layout.buildDirectory.dir("../../build").get()
rootProject.layout.buildDirectory.set(newBuildDir)

allprojects {
    repositories {
        google()
        mavenCentral()
    }
}

subprojects {
    val newSubprojectBuildDir: Directory = newBuildDir.dir(project.name)
    project.layout.buildDirectory.set(newSubprojectBuildDir)
}

subprojects {
    project.evaluationDependsOn(":app")
}

tasks.register<Delete>("clean") {
    delete(rootProject.layout.buildDirectory)
}