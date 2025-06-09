marcador=0
        
        if sensor!= Color.GRAY:
            if sensor== Color.MY_YELLOW:
                drive_base.straight(-125)
                direcao = virarPara('B')
                sensor = verificarFrente()
                if sensor!= Color.GRAY :
                    linha, coluna = frente (linha, coluna)
                    tabuleiro[linha][coluna]=color_sensorE.color()
                    direcao = virarPara(di)
                    sensor = verificarFrente()
                    linha, coluna = frente (linha, coluna)
                    tabuleiro[linha][coluna]=color_sensorE.color()
                    sensor = verificarFrente()
                    if sensor== Color.GRAY:
                        direcao = virarPara(do)
                        marcador=1
                        coluna=5
                    else:
                        sensor = verificarFrente()
                        linha, coluna = frente (linha, coluna)
                        tabuleiro[linha][coluna]=color_sensorE.color()
                        direcao = virarPara('C')
                        sensor = verificarFrente()
                        linha, coluna = frente (linha, coluna)
                        tabuleiro[linha][coluna]=color_sensorE.color()
                        direcao = virarPara(di)
                else:
                    direcao = virarPara('C')
                    sensor = verificarFrente()
                    linha, coluna = frente (linha, coluna)
                    tabuleiro[linha][coluna]=color_sensorE.color()
                    direcao = virarPara(di)
                    sensor = verificarFrente()
                    linha, coluna = frente (linha, coluna)
                    tabuleiro[linha][coluna]=color_sensorE.color()
                    sensor = verificarFrente()
                    if sensor==Color.GRAY:
                        direcao = virarPara(do)
                        marcador=1
                    else:
                        sensor = verificarFrente()
                        linha, coluna = frente (linha, coluna)
                        tabuleiro[linha][coluna]=color_sensorE.color()
                        direcao = virarPara('B')
                        sensor = verificarFrente()
                        linha, coluna = frente (linha, coluna)
                        tabuleiro[linha][coluna]=color_sensorE.color()
                        direcao = virarPara(di)

            else:
                linha, coluna = frente (linha, coluna)
                tabuleiro[linha][coluna]=color_sensorE.color()

    if marcador==0:
        direcao = virarPara('B')
