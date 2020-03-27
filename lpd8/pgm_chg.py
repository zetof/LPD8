class Pgm_Chg:
    """
    A class defining all possible values for a program change event
    Also makes an array containing all program change IDs and defines the maximum number of available program changes
    """

    PGM_CHG_1 = 1
    PGM_CHG_2 = 2
    PGM_CHG_3 = 3
    PGM_CHG_4 = 4
    PGM_CHG_5 = 5
    PGM_CHG_6 = 6
    PGM_CHG_7 = 7
    PGM_CHG_8 = 8

    ALL_PGM_CHG = [PGM_CHG_1, PGM_CHG_2, PGM_CHG_3, PGM_CHG_4, PGM_CHG_5, PGM_CHG_6, PGM_CHG_7, PGM_CHG_8]
    PGM_MAX = len(ALL_PGM_CHG)
