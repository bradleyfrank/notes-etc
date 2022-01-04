# Groovy

```groovy
// returns exit code and result of shell command

def runCommand(script) {    
    echo "[runCommand:script] ${script}"

    def stdoutFile = "rc.${BUILD_NUMBER}.out"    
    script = script + ' > ' + stdoutFile

    def res = [:]    
    res['exitCode'] = sh(returnStatus: true, script: script)    
    res['stdout'] = sh(returnStdout: true, script: 'cat ' + stdoutFile)

    sh(returnStatus: true, script: 'rm -f ' + stdoutFile)

    echo "[runCommand:response] ${res}"    
    return res
}
```

