# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 15:46:50 2021

@author: Filip Šimáně
"""
import os
import sys
import platform


class Svg:
    """
    Třída která obsahuje metody pro načtení vzorového dokumentu, zpracování a export.
    """

    def __init__(self, import_file_path: str, export_folder_path: str):
        """
        U vstupních proměných jsou definovány datové typy, bez základních hodnot.
        """
        self.import_path = import_file_path
        self.export_path = export_folder_path

    def generate_svg_files(self):
        """
        Hlavní metoda, která se spouští v případě zadání správných parametrů do konzole. Spouští interní metody.
        """
        self._open_file()
        self._get_all_combinations()
        self._get_svg_header()
        self._generate_files()

    def _open_file(self):
        """
        Otevření a uložení importovaného Svg souboru do proměnné.
        """
        with open(self.import_path, "r") as f:
            self.svg_file = f.readlines()

    def _get_all_combinations(self):
        """
        Získání všech kombinací ze vzorového souboru.
        """
        id_array = []

        # Hledej všechny řádky v souboru, které obsahují "id=", 
        # řádek rozděl po mezerách, ulož do listu a vezmi druhý prvek (id=...)
        for line in self.svg_file:
            if "id=" in line:
                id_array.append(line.split(" ")[1])

        self.array_of_colors = []
        self.array_of_id = []

        # Vyfiltruj všechny prvky, které obsahují "id", nebo barvu "Basic" a ulož je 
        # do array_of_id, nebo array_of_colors, všechno ostatní ignoruj
        for item in id_array:
            if "Basic" in item:
                temp = item.split("\"")[-2]
                if temp != '':
                    self.array_of_colors.append(temp)
            if "id" in item:
                temp = item.split("\"")[-1]
                if temp != '':
                    self.array_of_id.append(temp)

    def _get_svg_header(self):
        """
        Získání záhlaví a zápatí z originálního svg souboru.
        """
        self.svg_header = ""
        self.svg_footer = "</svg>"

        # Všechno řádky až po '</style>' považuj za header a ulož do proměnné svg_header
        for line in self.svg_file:
            self.svg_header += line
            if '</style>' in line:
                break

    def _generate_files(self):
        """
        Metoda generující všechny možné kombinace Svg obrázků.
        return: None
        """
        # Pro každou barvu vytvoř ikonu s každým dostupným číslem
        for color in self.array_of_colors:
            for id_number in self.array_of_id:
                
                new_file = ""
                new_file += self.svg_header

                # Pro každý řádek v proměnné svg_file zjistil jestli obsahuje aktuální color a id
                for line in self.svg_file:
                    if color in line:
                        new_file += line
                    if "id=\"" + id_number in line:
                        new_file += line
                new_file += self.svg_footer
                
                if platform.system() == 'Windows':
                    ikona = open(f"{self.export_path}\{color}_{id_number}.svg", "w")
                else:
                    ikona = open(f"{self.export_path}/{color}_{id_number}.svg", "w")
                    
                ikona.writelines(new_file)
                ikona.close()
                self._progress(color=color, id_number=id_number)

    @staticmethod
    def _progress(color, id_number):
        """
        Vypisuje jednoltivé jména souborů, které se vytvářejí.
        """
        print(f"Exporting file {color}_{id_number}.svg")

    @staticmethod
    def help__():
        """
        Zobrazí se zadáním "--help", který následně vypíše napovědu pro správé použití programu.
        """
        print("Define export path of generated SVGs by --export-path [path] "
              "and import path of the svg file --import-file [path]")

    @staticmethod
    def error(input_string):
        """
        Výchozí chybová hláška, která se spouští pokud uživatel zadá nesprávnou syntaxi. Vypíše příkaz "--help".

        """
        print(f'Try typing "--help". {input_string}')


if __name__ == "__main__":

    if "--help" in sys.argv:
        Svg.help__()
    
    # Ošetření chyb v případě, že uživatel neposkytl dostatek vstupních parametů
    elif len(sys.argv) == 5:
        # Kontrola, že uživatel zadal správné parametry
        if sys.argv[1] == "--export-path" and sys.argv[3] == "--import-file":

            import_path = sys.argv[4]
            export_path = sys.argv[2]

            # Kontrola, že importovaný soubor je k dispozici, případně konec programu a vyhození chyby
            if not os.path.isfile(import_path):
                raise Exception("File doesnt exist")

            # Kontrola, že složka pro export je k dispozici, případně vytvoření složky
            if not os.path.isdir(export_path):
                os.mkdir(export_path)

            # Vytvoření objektu třídy Svg a předání parametrů import_path a export_path
            svg_generator = Svg(import_file_path=import_path, export_folder_path=export_path)
            
            # Volání metody pro zpracování vstupních parametrů a export ikon/obrázků
            svg_generator.generate_svg_files()

        # V případě nesplnění vstupních podmínek dojde k výpisu chybové hlášky
        else:
            Svg.error("Order of input parameters does not match or wrong name")
            
    # V případě nesplnění vstupních podmínek dojde k výpisu chybové hlášky
    else:
        Svg.error("Wrong number of input parameters")