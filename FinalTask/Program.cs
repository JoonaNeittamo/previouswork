using System;
using System.Collections.Generic;

namespace DeckOfCards
{
    class Program
    {
        static void Main(string[] args)
        {
            Trick trick = new Trick();
            Console.Clear();
            trick.GameStart();
            // Console.WriteLine("Welcome to 'Simplified version of the game Trick' !");
            // Console.Write("Write START to start: ");
            // string chooseStart = Console.ReadLine();

            // if (chooseStart == "START") {
            //     trick.GameStart();
            // }
            // else {
            //     Main(null);
            // }

        }
    }
}
