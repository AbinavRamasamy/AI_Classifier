#!/bin/bash

# Activate virtual environment
source .venv/bin/activate

# List of 100 robotic, clean, sans-serif fonts (no cursive)
fonts=(
    "Roboto" "Open-Sans" "Lato" "Montserrat" "Source-Sans-Pro"
    "Roboto-Condensed" "Oswald" "Raleway" "Ubuntu" "Nunito-Sans"
    "Titillium-Web" "PT-Sans" "Oxygen" "Arimo" "IBM-Plex-Sans"
    "Noto-Sans" "Work-Sans" "Fira-Sans" "Inter" "DM-Sans"
    "Poppins" "Rubik" "Karla" "Nunito" "Muli" "Barlow"
    "Public-Sans" "Red-Hat-Display" "Manrope" "Outfit" "Sora"
    "Space-Grotesk" "Urbanist" "Plus-Jakarta-Sans" "Lexend"
    "Commissioner" "Epilogue" "Instrument-Sans" "Schibsted-Grotesk"
    "JetBrains-Mono" "Source-Code-Pro" "Fira-Code" "Roboto-Mono"
    "Ubuntu-Mono" "Inconsolata" "IBM-Plex-Mono" "Space-Mono"
    "Archivo" "Exo" "Exo-2" "Quantico" "Rajdhani" "Electrolize"
    "Gruppo" "Michroma" "Audiowide" "Syncopate" "Iceberg" "Jura"
    "Orbitron" "Saira" "Saira-Condensed" "Saira-Extra-Condensed"
    "Abel" "Advent-Pro" "Alata" "Alef" "Armata" "Assistant"
    "Atomic-Age" "B612" "B612-Mono" "Basic" "BenchNine" "Blinker"
    "Bruno-Ace" "Cabin" "Chakra-Petch" "Changa" "Chivo" "Comfortaa"
    "Cuprum" "Cutive-Mono" "Days-One" "Dosis" "Economica" "Encode-Sans"
    "Encode-Sans-Condensed" "Federo" "Francois-One" "Goldman" "Gudea"
    "Hammersmith-One" "Hind" "Hind-Siliguri" "Iceland" "Inder" "K2D"
    "Kanit" "Khand" "Lekton" "Maven-Pro" "Merriweather-Sans" "Monda"
)

echo "🚀 Installing ${#fonts[@]} robotic fonts using google-fonts install..."

successful=0
failed=0

for font in "${fonts[@]}"; do
    echo "📥 Installing $font..."
    
    if google-fonts install "$font"; then
        echo "✅ $font installed successfully"
        ((successful++))
    else
        echo "❌ Failed to install $font"
        ((failed++))
    fi
    
    # Small delay to be respectful
    sleep 2
done

echo ""
echo "🎉 Installation Summary:"
echo "✅ Successfully installed: $successful fonts"
echo "❌ Failed installations: $failed fonts"
echo "📁 Fonts should be installed in your system fonts directory"
