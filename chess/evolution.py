"""
{
    'chessmans_moves': {
        'WE00': [],
        'WH01': ['20', '22'], 
        'WC02': [], 
        'WQ03': ['14', '25', '36', '47'], 
        'WK04': ['14', '05'], 
        'WH06': ['25', '27', '14'], 
        'WE07': [], 
        'WS10': ['20', '30'], 
        'WS11': ['21', '31'], 
        'WS12': ['22', '32'], 
        'WS13': ['23', '33'], 
        'WS15': ['25', '35'], 
        'WS16': ['26', '36'], 
        'WS17': ['27', '37'], 
        'WS14': ['44'], 
        'WC05': ['50', '52', '63', '30', '32', '23', '14', '05']
    }, 
    'chessmans_positions': {
        'WE00': '00', 'WH01': '01', 'WC02': '02', 'WQ03': '03', 'WK04': '04', 'WH06': '06', 'WE07': '07', 
        'WS10': '10', 'WS11': '11', 'WS12': '12', 'WS13': '13', 'WS15': '15', 'WS16': '16', 'WS17': '17', 'WS14': '34', 'WC05': '41'
    }, 
    'avail_chessmans': ['WE00', 'WH01', 'WC02', 'WQ03', 'WK04', 'WH06', 'WE07', 'WS10', 'WS11', 'WS12', 'WS13', 'WS15', 'WS16', 'WS17', 'WS14', 'WC05'], 
    
    'block_possible_moves': {
        'WE00': ['10', '01'], 
        'WH01': ['13'], 
        'WC02': ['11', '13'], 
        'WQ03': ['13', '02', '04', '12'], 
        'WK04': ['03', '13', '15'], 
        'WH06': [], 
        'WE07': ['17', '06'], 
        'WS10': [], 
        'WS11': [], 
        'WS12': [], 
        'WS13': [], 
        'WS15': [], 
        'WS16': [], 
        'WS17': [], 
        'WS14': [], 
        'WC05': []
    }, 
    'all_moves': ['20', '22', '14', '25', '36', '47', '14', '05', '25', '27', '14', '21', '20', '22', 
                '21', '23', '22', '24', '24', '26', '25', '27', '26', '43', '45', '50', '52', '63', '30', '32', '23', '14', '05'], 

    'additional_data': {
        'box_backups': {
            '10': ['WE00'], 
            '01': ['WE00'], 
            '13': ['WH01', 'WC02', 'WQ03', 'WK04'], 
            '11': ['WC02'], 
            '02': ['WQ03'], 
            '04': ['WQ03'], 
            '12': ['WQ03'], 
            '03': ['WK04'], 
            '15': ['WK04'], 
            '17': ['WE07'], 
            '06': ['WE07']
        }, 
        'chessmans_can_move_to_box': {
            '20': ['WH01', 'WS10'], 
            '22': ['WH01', 'WS12'], 
            '14': ['WQ03', 'WK04', 'WH06', 'WC05'], 
            '25': ['WQ03', 'WH06', 'WS15'], 
            '36': ['WQ03', 'WS16'], 
            '47': ['WQ03'], 
            '05': ['WK04', 'WC05'], 
            '27': ['WH06', 'WS17'], 
            '30': ['WS10', 'WC05'], 
            '21': ['WS11'], 
            '31': ['WS11'], 
            '32': ['WS12', 'WC05'], 
            '23': ['WS13', 'WC05'], 
            '33': ['WS13'], 
            '35': ['WS15'], 
            '26': ['WS16'], 
            '37': ['WS17'], 
            '44': ['WS14'], 
            '50': ['WC05'], 
            '52': ['WC05'], 
            '63': ['WC05']
        }, 
        'provide_threats_to_opp': {
            'WC05': ['50', '63']
        }
    }, 
    'after_stop_moves': {
        'WE00': ['10', '20', '30', '40', '50', '01', '02'], 
        'WH01': [], 
        'WC02': ['11', '20', '13', '24', '35', '46', '57'], 
        'WQ03': ['13', '23', '33', '43', '53', '63', '02', '01', '04', '05', '06', '12', '21', '30'], 
        'WK04': [], 
        'WH06': [], 
        'WE07': ['17', '27', '37', '47', '57', '67', '06', '05', '04'], 
        'WS10': [], 
        'WS11': [], 
        'WS12': [], 
        'WS13': [], 
        'WS15': [], 
        'WS16': [], 
        'WS17': [], 
        'WS14': [], 
        'WC05': ['50', '63', '74']
    }, 
    'btw_moves': {}, 
    'guarding_chessman_can_move': {}, 
    'legal_moves': {
        'WH01': ['20', '22'], 
        'WQ03': ['14', '25', '36', '47'], 
        'WK04': ['14', '05'], 
        'WH06': ['25', '27', '14'], 
        'WS10': ['20', '30'], 
        'WS11': ['21', '31'], 
        'WS12': ['22', '32'], 
        'WS13': ['23', '33'], 
        'WS15': ['25', '35'], 
        'WS16': ['26', '36'], 
        'WS17': ['27', '37'], 
        'WS14': ['44'], 
        'WC05': ['50', '52', '63', '30', '32', '23', '14', '05']
    }, 
    'kp': '04', 
    'color': 'W'
}

1. my_block_possible_moves -> dictionary of list of my chessmans positons whom the my chessman is providing backup 
example -->my_block_possible_moves = {'BQ75':['74','45'],'BH76':['57'],...}

2. my_chessman_moves --> dictionary of my chessman list of possible moves
example --> {'BQ75':['64','54','44','53'],...} 

3. my_chessman_position --> dictionary of my chessman current position
example --> {'BQ75':'75', 'BS61':'41'}

4. safe boxes --> it is method who will provide list of safe boxes for particuler chessman from his curret_position where he won't got killed
example --> for my_king --> ['76',71]

5. my_threats_after_move --> 'dictionary of my chessmans who are in threats after move with the lossing point with currennt position'
example  --> {'BQ75':9, 'BH72':3}

6. my_additional_data['box_backup'] --> dictionary of my chessmans postion whom list of my chessmans are providing backup.
like at box '55' my 'BH71' chessman is present the list of my chessmans are providing backup
example --> {'55':['BE71', 'BS64', ], '61':['BS62','BC72']}

7. my_additional_data['provide_threats_to_opp'] --> dicitionary of my chessmans who are providing threats to list of opponent chessman
here we store opponent chessman position rather the chessman_id(like here my queen is providing threats to list of opponent chessmans(box_id))
example --> {'BQ75': ['25','00','45'], 'BH72':[33,41]}

8. my_additional_data['chessmans_can_move_to_box'] --> on particuler box list of my_chessmans can moves. 
(dictionary of boxes where list of my chessmans can move it won't include the positons of my own chessma that are blocking to particuler boxes
(below example at box '03' list of my chessmans can move to)
example --> {'03':['BE70','BC75'], '02':['BS62'], ...}

9. my_additional_data['']

10. my_btw_moves = are list of moves where my chessmnas can move and there king from check(getting killed)
        my_btw_moves = {opp_threatning_chessman_id:[list of box that can block threat], ... }

11. my_guarding_chessman_can_moves ==> is list of boxes where guarding chessman can moves 
    cause if he move then my king will be in check that's why he had limitation on his moves
        my_guarding_chessman_can_moves = {guarding_chessman_id : [list of boxes where he can move], ... }

Tactical Opportunities:
Look for tactical opportunities, such as forks, pins, skewers, and other tactical motifs that could lead to a material advantage.
"""
