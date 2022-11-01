package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"os/exec"
	"strings"
)

func main() {

	fmt.Println("Argos")
	fmt.Println("''''''''''")
	fmt.Println(exec.Command("iwconfig"))
	fmt.Println("Which NIC would you like to use?")

	//Read Users NIC selection and save it
	reader := bufio.NewReader(os.Stdin)
	// ReadString will block until the delimiter is entered
	input, err := reader.ReadString('\n')
	if err != nil {
		fmt.Println("An error occured while reading input. Please try again", err)
		return
	}
	// remove the delimeter from the string
	input = strings.TrimSuffix(input, "\n")

	// run bettercap on the selected NIC
	cmd := exec.Command("sudo bettercap", "-iface", input)
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	err = cmd.Run()
	if err != nil {
		log.Fatalf("cmd.Run() failed with %s\n", err)
	}

	//start monitoring on the selected NIC  TODO: capture output and run as a subprocess
	//os.system("sudo bettercap -iface " + selectedNIC)
	//os.system("wifi.recon on")
}
