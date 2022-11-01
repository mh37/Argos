package main

import (
	"bufio"
	"fmt"
	"os"
	"os/exec"
	"strings"
)

func main() {

	fmt.Println("Argos")
	fmt.Println("''''''''''")
	fmt.Println(exec.Command("bash", "-c", "iwconfig").Output())
	fmt.Println("Which NIC would you like to use?")
	reader := bufio.NewReader(os.Stdin)
	// ReadString will block until the delimiter is entered
	input, err := reader.ReadString('\n')
	if err != nil {
		fmt.Println("An error occured while reading input. Please try again", err)
		return
	}
	// remove the delimeter from the string
	input = strings.TrimSuffix(input, "\n")

	cmd, err := exec.Command("bash", "-c", "sudo bettercap -iface ", input).Output()
	fmt.Println(cmd)

	if err != nil {
		fmt.Println(err)
	}

	//start monitoring on the selected NIC  TODO: capture output and run as a subprocess
	//os.system("sudo bettercap -iface " + selectedNIC)
	//os.system("wifi.recon on")
}
