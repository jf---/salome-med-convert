
.PHONY: all tetgen zset systus ansys salome aster abaqus clean reset

tetgen: 

	ln -sf config_tetgen.tex params.tex
	pdflatex tetra4.tex
	pdflatex tri3.tex
	pdflatex tetgen_connectivity.tex
	make clean

zset: 

	ln -sf config_zset.tex params.tex
	pdflatex hexa20.tex
	pdflatex hexa8.tex
	pdflatex penta15.tex
	pdflatex penta6.tex
	pdflatex pyra13.tex
	pdflatex pyra5.tex
	pdflatex quad4.tex
	pdflatex quad8.tex
	pdflatex seg2.tex
	pdflatex seg3.tex
	pdflatex tetra10.tex
	pdflatex tetra4.tex
	pdflatex tri3.tex
	pdflatex tri6.tex
	pdflatex zset_connectivity.tex
	make clean

systus: 

	ln -sf config_systus.tex params.tex
	pdflatex hexa20.tex
	pdflatex hexa8.tex
	pdflatex penta15.tex
	pdflatex penta6.tex
	pdflatex pyra13.tex
	pdflatex pyra5.tex
	pdflatex quad4.tex
	pdflatex quad8.tex
	pdflatex seg2.tex
	pdflatex seg3.tex
	pdflatex tetra10.tex
	pdflatex tetra4.tex
	pdflatex tri3.tex
	pdflatex tri6.tex
	pdflatex systus_connectivity.tex
	make clean

ansys: 

	ln -sf config_ansys.tex params.tex
	pdflatex hexa20.tex
	pdflatex hexa8.tex
	pdflatex penta15.tex
	pdflatex penta6.tex
	pdflatex pyra13.tex
	pdflatex pyra5.tex
	pdflatex quad4.tex
	pdflatex quad8.tex
	pdflatex seg2.tex
	pdflatex seg3.tex
	pdflatex tetra10.tex
	pdflatex tetra4.tex
	pdflatex tri3.tex
	pdflatex tri6.tex
	pdflatex ansys_connectivity.tex
	make clean


salome: 

	ln -sf config_salome.tex params.tex
	pdflatex hexa27.tex
	pdflatex hexa20.tex
	pdflatex hexa8.tex
	pdflatex penta18.tex
	pdflatex penta15.tex
	pdflatex penta6.tex
	pdflatex pyra13.tex
	pdflatex pyra5.tex
	pdflatex quad4.tex
	pdflatex quad8.tex
	pdflatex quad9.tex
	pdflatex seg2.tex
	pdflatex seg3.tex
	pdflatex seg4.tex
	pdflatex tetra10.tex
	pdflatex tetra4.tex
	pdflatex tri3.tex
	pdflatex tri6.tex
	pdflatex tri7.tex
	pdflatex salome_connectivity.tex
	make clean

aster: 

	ln -sf config_aster.tex params.tex
	pdflatex hexa27.tex
	pdflatex hexa20.tex
	pdflatex hexa8.tex
	pdflatex penta18.tex
	pdflatex penta15.tex
	pdflatex penta6.tex
	pdflatex pyra13.tex
	pdflatex pyra5.tex
	pdflatex quad4.tex
	pdflatex quad8.tex
	pdflatex quad9.tex
	pdflatex seg2.tex
	pdflatex seg3.tex
	pdflatex seg4.tex
	pdflatex tetra10.tex
	pdflatex tetra4.tex
	pdflatex tri3.tex
	pdflatex tri6.tex
	pdflatex tri7.tex
	pdflatex aster_connectivity.tex
	make clean

abaqus: 

	ln -sf config_abaqus.tex params.tex
	pdflatex hexa27.tex
	pdflatex hexa20.tex
	pdflatex hexa8.tex
	pdflatex penta18.tex
	pdflatex penta15.tex
	pdflatex penta6.tex
	pdflatex pyra13.tex
	pdflatex pyra5.tex
	pdflatex quad4.tex
	pdflatex quad8.tex
	pdflatex quad9.tex
	pdflatex seg2.tex
	pdflatex seg3.tex
	pdflatex tetra10.tex
	pdflatex tetra4.tex
	pdflatex tri3.tex
	pdflatex tri6.tex
	pdflatex abaqus_connectivity.tex
	make clean

clean:
	rm -f *.aux *.log params.tex

reset :
	make clean
	rm -f *.pdf

all :
	make tetgen zset systus ansys salome aster abaqus
