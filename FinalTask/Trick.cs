using System;
using System.Collections.Generic;

namespace DeckOfCards
{
    class Trick
    {
        public void GameStart()
        {
            Console.Clear();
            Console.WriteLine("Game started!");
            
            Deck deck = new Deck();
            
            deck.Shuffle();

            List<Card> drawn = new List<Card>();

            PlayerChooseDraw();
            
            
        }
        public void PlayerChooseDraw()
        {
            
            Deck deck = new Deck();
            Console.WriteLine("Number of cards in the deck is: " + deck.CardCount);
            Console.WriteLine("-------------");
            Console.WriteLine("You can draw between 1 to 26");
            Console.Write("Draw amount: ");
            int playerDraw = Convert.ToInt32(Console.ReadLine());

            if (playerDraw > 26) {
                Console.Clear();
                Console.WriteLine("ERROR: Maximum cards to draw is 26 !");
                PlayerChooseDraw();
            }
            else if (playerDraw < 1) {
                Console.Clear();
                Console.WriteLine("ERROR: Minimum cards to draw is 1 !");
                PlayerChooseDraw();
            }
            else {
                Console.Clear();
                DeckCreation(playerDraw);         
            }
        }
        public void DeckCreation(int playerDraw) 
        {
            Deck deck = new Deck();
            List<string> playerlist = new List<string>();
            List<string> opponentlist = new List<string>();

            // DRAW CARDS TO PLAYER HAND
            int i = 0;
            while (i < playerDraw) {
                deck.Shuffle();     
                playerlist.Add(deck.Cards[0].Print());
                i++;
            }

            // DRAW CARDS TO OPPONENT HAND
            int i2 = 0;
            while (i2 < playerDraw) {
                deck.Shuffle();     
                opponentlist.Add(deck.Cards[0].Print());
                i2++;
            }

            Console.WriteLine("Cards have been drawn!");

            PlayerChooseCard(playerDraw, playerlist, opponentlist);
        }
        
        public void PlayerChooseCard(int playerDraw, System.Collections.Generic.List<string> playerlist, System.Collections.Generic.List<string> opponentlist)
        {
            System.Random random = new System.Random(); 

            int playerScore = 0;
            int opponentScore = 0;

            while (playerDraw >= 1) {
            
                Console.WriteLine("On the right you can see the index number to know which card you will use.");
                Console.WriteLine("-------------------");
                Console.WriteLine($"PLAYER {playerScore} - {opponentScore} OPPONENT");
                Console.WriteLine("-------------------");
                Console.WriteLine("CURRENT HAND");
                Console.WriteLine(playerDraw);

                // SHOW PLAYER HAND
                int i3 = 0;
                while (i3 < playerDraw) {
                    Console.Write(playerlist[i3]);
                    Console.WriteLine($" |||||||| {i3}");
                    i3++;
                }
                
                // // FOR TESTING IF RANDOMNESS WORKS (SHOWS OPPONENT HAND)
                // Console.WriteLine("-------------------");
                // Console.WriteLine("OPPONENT HAND");
                // int i4 = 0;
                // while (i4 < playerDraw) {
                //     Console.Write(opponentlist[i4]);
                //     Console.WriteLine($" |||||||| {i4}");
                //     i4++;
                // }

                Console.WriteLine("");
                Console.Write("Which card to use: ");
                int playerUseCard = Convert.ToInt32(Console.ReadLine());

                if (playerUseCard < playerDraw) {

                    int opponentUseCard = random.Next(0,playerDraw);
                    int playerJustWon = 1;
                    

                    // SHOW AND REMOVE CARDS
                    
                    Console.WriteLine("Player chose: " + playerlist[playerUseCard]);
                    Console.WriteLine("Opponent chose: " + opponentlist[opponentUseCard]);
                    
                    
                    Console.WriteLine("");


                    var lines = playerlist[playerUseCard].Split(' ');
                    string playerSuit = lines[lines.Length - 1];
                    string playerRank = playerlist[playerUseCard].Split(' ')[0];

                    var lines2 = opponentlist[opponentUseCard].Split(' ');
                    string opponentSuit = lines2[lines2.Length - 1];
                    string opponentRank = opponentlist[opponentUseCard].Split(' ')[0];

                    int playerRankUsable = Convert.ToInt32(playerRank);
                    int opponentRankUsable = Convert.ToInt32(opponentRank);
                    

                    if (opponentSuit == playerSuit && opponentRankUsable > playerRankUsable) {

                        int opponentWinning = 1;
                        playerlist.RemoveAt(playerUseCard);
                        opponentlist.RemoveAt(opponentUseCard);
                        playerDraw--;
                        Console.WriteLine("Opponent wins because he had higher card rank!");

                        while (opponentWinning == 1) {

                            
                            
                            opponentScore++;
                            
                            Console.Write("Press ENTER to continue");
                            Console.ReadLine();
                            Console.Clear();

                            Console.WriteLine("On the right you can see the index number to know which card you will use.");
                            Console.WriteLine("-------------------");
                            Console.WriteLine($"PLAYER {playerScore} - {opponentScore} OPPONENT");
                            Console.WriteLine("-------------------");
                            Console.WriteLine("CURRENT HAND");

                            int i3_insideloop = 0;
                            while (i3_insideloop < playerDraw) {
                                Console.Write(playerlist[i3_insideloop]);
                                Console.WriteLine($" |||||||| {i3_insideloop}");
                                i3_insideloop++;
                            }
                            
                            Console.WriteLine("");
                            int opponentUseCard_insideloop = random.Next(0,playerDraw);
                            Console.WriteLine("Opponent chose: " + opponentlist[opponentUseCard_insideloop]);
                            Console.Write("Which card to use: ");
                            int playerUseCard_insideloop = Convert.ToInt32(Console.ReadLine());

                            if (playerUseCard_insideloop < playerDraw) {
                                Console.WriteLine("Player chose: " + playerlist[playerUseCard_insideloop]);

                                var lines_insideloop = playerlist[playerUseCard_insideloop].Split(' ');
                                string playerSuit_insideloop = lines_insideloop[lines_insideloop.Length - 1];
                                string playerRank_insideloop = playerlist[playerUseCard_insideloop].Split(' ')[0];

                                var lines2_insideloop = opponentlist[opponentUseCard_insideloop].Split(' ');
                                string opponentSuit_insideloop = lines2_insideloop[lines2_insideloop.Length - 1];
                                string opponentRank_insideloop = opponentlist[opponentUseCard_insideloop].Split(' ')[0];

                                int playerRankUsable_insideloop = Convert.ToInt32(playerRank_insideloop);
                                int opponentRankUsable_insideloop = Convert.ToInt32(opponentRank_insideloop);

                                    if (opponentSuit_insideloop == playerSuit_insideloop && opponentRankUsable_insideloop > playerRankUsable_insideloop) {
                                        playerlist.RemoveAt(playerUseCard_insideloop);
                                        opponentlist.RemoveAt(opponentUseCard_insideloop);
                                        playerDraw--;
                                        Console.WriteLine("Opponent wins because he had higher card rank!");
                                        if (playerDraw > 0) {
                                        }
                                        else {
                                            opponentWinning--;
                                        }
                                    }
                                    else if (opponentSuit_insideloop == playerSuit_insideloop && opponentRankUsable_insideloop < playerRankUsable_insideloop) {
                                        Console.WriteLine("Player wins because he had higher card rank!");
                                        playerScore++;
                                        opponentWinning--;
                                        playerJustWon--;
                                        playerlist.RemoveAt(playerUseCard_insideloop);
                                        opponentlist.RemoveAt(opponentUseCard_insideloop);
                                    }
                                    else if (playerSuit_insideloop != opponentSuit_insideloop) {
                                        playerlist.RemoveAt(playerUseCard_insideloop);
                                        opponentlist.RemoveAt(opponentUseCard_insideloop);
                                        playerDraw--;
                                        Console.WriteLine("Opponent wins because Player did not have the same suit!");
                                        if (playerDraw > 0) {
                                        }
                                        else {
                                            opponentWinning--;
                                        }

                                    }
                                    else if (opponentSuit_insideloop == playerSuit_insideloop && opponentRankUsable_insideloop == playerRankUsable_insideloop) {
                                        playerlist.RemoveAt(playerUseCard_insideloop);
                                        opponentlist.RemoveAt(opponentUseCard_insideloop);
                                        playerDraw--;
                                        
                                        if (playerDraw > 0) {
                                        }
                                        else {
                                            opponentWinning--;
                                        }    
                                    
                                    
                                    }    
                                    else if (playerDraw == 0) {
                                        opponentWinning--;
                                    }         

                            }
                            else {
                                Console.Clear();
                                Console.WriteLine("ERROR: That card is not in the index range!");
                            }
                        }
                    }
                    else if (opponentSuit == playerSuit && opponentRankUsable < playerRankUsable) {
                        Console.WriteLine("Player wins because he had a higher card rank!");
                        playerScore++;
                    }
                    else if (opponentSuit != playerSuit) {
                        Console.WriteLine("Player wins because Opponent did not have the same suit!");
                        playerScore++;
                    }
                    
                    


                    
                    
                    if (playerJustWon == 1) {

                        if (playerDraw >= 1) {
                            Console.Write("Press ENTER to continue");
                            playerlist.RemoveAt(playerUseCard);
                            opponentlist.RemoveAt(opponentUseCard);
                            Console.ReadLine();
                            Console.Clear();
                            playerDraw--;
                        }
                        
                        else {}

                    }
                    else {
                        Console.Write("Press ENTER to continue");
                        Console.ReadLine();
                        Console.Clear();
                        if (playerDraw >= 1) {
                            playerDraw--;
                        }
                        else {}
                    }
                }
                
                else {
                    Console.Clear();
                    Console.WriteLine("ERROR: That card is not in the index range!");
                }
            }

            if (playerScore > opponentScore) {
                Console.Clear();
                Console.WriteLine("PLAYER WINS THE GAME!");
                Console.WriteLine($"PLAYER {playerScore} - {opponentScore} OPPONENT");
            }

            else if (playerScore < opponentScore) {
                Console.Clear();
                Console.WriteLine("OPPONENT WINS THE GAME!");
                Console.WriteLine($"PLAYER {playerScore} - {opponentScore} OPPONENT");
            }

            else {
                Console.Clear();
                Console.WriteLine("GAME IS A TIE!");
                Console.WriteLine($"PLAYER {playerScore} - {opponentScore} OPPONENT");
                Console.WriteLine("I dont even think its possible to get this screen...");
            }



        }

        
    }
}