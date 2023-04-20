
Skip Types
----------
This option allows to pass a comma separated list to the converter. Each item of the list is a type of cell ( specified in the input format ) to be ignored at conversion.

Supported formats : Systus.

Systus cells type format
************************
The Systus format for a cell uses a 4-digit key, as for `3020` for an `HEXA20` cell.
The digits are divided into 3 parts :

   #. The first digit `3`, which varies within the range [0-3] and indicates the cell dimension

   #. The second digit `0`, which varies within the range [0-9] and indicates the cell format ( geometric, contact, link, etc...). Formats in the range [4-9] are not supported for the automatic conversion : the user must choose to ignore them, or must modify manually the mesh file.

   #. The last two digits `20` indicate the number of nodes of the cells.
