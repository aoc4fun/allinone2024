import scala.annotation.tailrec
import scala.util.matching.Regex
import scala.io.Source

class Day5 extends Puzzle:
  def name:String ="day5"

  def sample="""47|53
               |97|13
               |97|61
               |97|47
               |75|29
               |61|13
               |75|53
               |29|13
               |97|29
               |53|29
               |61|53
               |97|53
               |61|29
               |47|13
               |75|47
               |97|75
               |47|61
               |75|61
               |47|29
               |75|13
               |53|13
               |
               |75,47,61,53,29
               |97,61,53,29,13
               |75,29,13
               |75,97,47,61,53
               |61,13,29
               |97,13,75,29,47""".stripMargin.split("\\r?\\n").iterator

  def Puzzle1(l: Iterator[String]): Long = {
    val rules = parseRules(l)
    println(rules)
    val lists = l.map(_.split(",").map(_.toInt).toList).toList
    println(lists.filter(checkOrder(_, rules)).toList)
    lists.filter(checkOrder(_, rules)).map(getMiddle(_)).sum
  }
  def Puzzle2(l: Iterator[String]): Long = 2

end Day5


def parseRules(l: Iterator[String]):List[(Int,Int)] =
  var result:List[(Int,Int)] = List()
  l.takeWhile(_.contains("|")).foldLeft(result){
    (list, s) => {
      val item = s.split("\\|")
      (item(0).toInt,item(1).toInt)::list
    }
  }

def checkOrder(l:List[Int], rules: List[(Int,Int)]):Boolean =
  rules.filter((n1,n2) => {
    if(l.contains(n1) && l.contains(n2)) then l.indexOf(n1) > l.indexOf(n2) else false
  }).isEmpty




def getMiddle(l:List[Int]):Int = l(l.size/2)

// 52,27,61,87,24
// 17,89,83,24,92

//List(48, 91, 86, 62, 58, 66, 39, 72, 19, 96, 15, 65, 63, 12, 41, 25, 46, 64, 75, 11, 95, 99, 23, 61, 36, 82, 89, 85, 24, 52, 88, 53, 28, 74, 87, 27, 18, 92, 26, 51, 67, 34, 83, 69, 93, 42, 17, 79, 22)