from preprocessing import no_words,no_reviews,no_validation,no_test,forest_trees,forest_tree_features
import math
import pickle
import random

class Node:
	def __init__(self,listpos,listneg,wordindex,l=0):
		self.parent=None
		self.left=None
		self.right=None
		self.poslist=listpos
		self.neglist=listneg
		self.indexword=wordindex
		self.label=None
		self.label=l
		if(wordindex==-1):
			self.leaf=True
		else:
			self.leaf=False

class tree:
	def __init__(self):
		self.root=None
	
	def treeconstruct(self,listpos,listneg,indexlist,review_list,height=no_words):
		self.root=self.construct(listpos,listneg,indexlist,review_list,height)

	def construct(self,listpos,listneg,indexlist,review_list,height):
		if(len(listneg)==0 or len(listpos)==0):
			if(len(listneg)==0):
				node=Node(listpos,[],-1,1)
			if(len(listpos)==0):
				node=Node([],listneg,-1,-1)
			return node							#returned leaf for single branch
		index=maxgain(listpos,listneg,indexlist,review_list)
		if(index==-1 or height==1):
			index=-1
			if(len(listpos)>=len(listneg)):
				node=Node(listpos,listneg,index,1)
			else:
				node=Node(listpos,listneg,index,-1)
			return node 						#returned leaf for zero gain
		node=Node(listpos,listneg,index)
		[pos,neg,not_pos,not_neg]=splitlist(listpos,listneg,index,review_list)
		node.left=self.construct(pos,neg,indexlist,review_list,height-1)
		if(node.left!=None):
			node.left.parent=node
		node.right=self.construct(not_pos,not_neg,indexlist,review_list,height-1)
		if(node.right!=None):
			node.right.parent=node
		return node

	def printtree(self,root):
		if(root==None):
			return
		print(root.indexword)
		print("leftpathtaken")
		self.printtree(root.left)
		print("rightpathtaken")
		self.printtree(root.right)	



def entropy(plen,nlen):
	if(plen==0 or nlen==0):
		return 0
	ppos=plen/(nlen+plen)
	pneg=nlen/(nlen+plen)
	return -(ppos*math.log(ppos,2)+pneg*math.log(pneg,2))
	

def gain(listpos,listneg,index,review_list):
	poscount=0
	negcount=0
	for i in listpos:
		if index in review_list[i]['list']:
			poscount=poscount+1
	for i in listneg:
		if index in review_list[i]['list']:
			negcount=negcount+1
	plen=len(listpos)
	nlen=len(listneg)
	plen_notpresent=plen-poscount
	nlen_notpresent=nlen-negcount
	g=entropy(plen,nlen) - ((poscount+negcount)/(plen+nlen))*entropy(poscount,negcount) - ((plen_notpresent+nlen_notpresent)/(plen+nlen))*entropy(plen_notpresent,nlen_notpresent)
	return g


def count_splitting_times(root,indexcount):
	if(root==None):
		return
	if root.indexword in indexcount:
		indexcount[root.indexword]=indexcount[root.indexword]+1
	else:
		indexcount[root.indexword]=1
	count_splitting_times(root.left,indexcount)
	count_splitting_times(root.right,indexcount)


def maxgain(listpos,listneg,indexlist,review_list):
	maxgain=0
	index=-1
	for i in indexlist:
		tempgain=gain(listpos,listneg,i,review_list)
		if(tempgain>=maxgain):
			maxgain=tempgain
			index=i
	if(maxgain==0):
		return -1
	return index


def splitlist(listpos,listneg,index,review_list):
	poscount=[]
	negcount=[]
	for i in listpos:
		if index in review_list[i]['list']:
			poscount.append(i)
	for i in listneg:
		if index in review_list[i]['list']:
			negcount.append(i)
	not_pos=[x for x in listpos if x not in poscount]
	not_neg=[x for x in listneg if x not in negcount]
	return [poscount,negcount,not_pos,not_neg]


def checksentiment(s,tree):
	node=tree.root
	while(node.leaf!=True):
		index=node.indexword
		if index in s['list']:
			node=node.left
		else:
			node=node.right
	return node.label

def checksentimentforest(s,treelist):
	sentiment=0
	for j in treelist:
		sentiment=sentiment+checksentiment(s,j)
	if(sentiment>=0):
		return 1
	else:
		return -1

def height(node):
    if (node == None):
        return 0 ; 
    else :
        lDepth = height(node.left)
        rDepth = height(node.right)
        if (lDepth > rDepth):
            return lDepth+1
        else:
            return rDepth+1

def accuracy(tree,reviewset,reviews):
	count=0
	for i in reviewset:
		temp=checksentiment(reviews[i],tree)
		if ((reviews[i]['sentiment']<=4 and temp==-1) or (reviews[i]['sentiment']>=7 and temp==1)):
			count=count+1
	return (count/len(reviewset))*100


def forest_accuracy(treelist,reviewset,reviews):
	count=0
	for i in reviewset:
		temp=checksentimentforest(reviews[i],treelist)
		if ((reviews[i]['sentiment']<=4 and temp==-1) or (reviews[i]['sentiment']>=7 and temp==1)):
			count=count+1
	return (count/len(reviewset))*100	

def pruning(tree,root,validation_list,validation_reviews):
	if(root==None):
		return
	if(root.leaf==True):
		return
	if(root.left.leaf==True and root.right.leaf==True):
		a1=accuracy(tree,validation_list,validation_reviews)
		root.leaf=True
		if len(root.poslist)>=len(root.neglist):
			root.label=1
		else:
			root.label=-1
		a2=accuracy(tree,validation_list,validation_reviews)
		if(a2>=a1):
			root.left=None
			root.right=None
			pruning(tree,root.parent,validation_list,validation_reviews)
		else:
			root.leaf=False
			root.label=0
		return
	else:
		pruning(tree,root.left,validation_list,validation_reviews)
		pruning(tree,root.right,validation_list,validation_reviews)
		return

def addnoice(poslist,neglist,p,review_list):
	no=(p/100)*(len(poslist)+len(neglist))
	p=poslist.copy()
	n=neglist.copy()
	ptemp=random.sample(p,int(no/2))
	ntemp=random.sample(n,int(no/2))
	p=[x for x in p if x not in ptemp]
	n=[x for x in n if x not in ntemp]
	for i in ptemp:
		review_list[i]['sentiment']=2
	for i in ntemp:
		review_list[i]['sentiment']=8
	p=p+ntemp
	n=n+ptemp
	return (p,n)

def count_nodes(node):
	if node==None:
		return 0
	if node.leaf==True:
		return 1
	return 1+count_nodes(node.left)+count_nodes(node.right)

def count_leaves(node):
	if(node.leaf==True):
		return 1
	else:
		return count_leaves(node.left)+count_leaves(node.right)
	

if __name__=="__main__":
	Tree=tree()
	Tree.treeconstruct(random_list_pos,random_list_neg,indexlist)
	

	print ("total nodes in decision tree initially : "+str(count_nodes(Tree.root)))
	print ("total leaves in decision tree initially : "+str(count_leaves(Tree.root)))

	print ("height of decision tree initially : "+str(height(Tree.root)))

	print ("accuracy on traning set : "+str(accuracy(Tree,(random_list_pos+random_list_neg),review_list)))
	print ("accuracy on test set : "+str(accuracy(Tree,test_list,test_reviews)))

	EarlyTree=tree()
	EarlyTree.treeconstruct(random_list_pos,random_list_neg,indexlist,90)

	print ("total nodes in training tree for early stopping: "+str(count_nodes(EarlyTree.root)))
	print ("total leaves in training tree early stopping: "+str(count_leaves(EarlyTree.root)))

	print ("accuracy on traning set early stopping:: "+str(accuracy(EarlyTree,(random_list_pos+random_list_neg),review_list)))
	print ("accuracy on test set early stopping: : "+str(accuracy(EarlyTree,test_list,test_reviews)))

	pruning(Tree,Tree.root,validation_list,validation_reviews)
	print ("total nodes in training tree after pruning: "+str(count_nodes(Tree.root)))
	print ("total leaves in training tree after pruning : "+str(count_leaves(Tree.root)))
	print ("accuracy on test set after pruning: "+str(accuracy(Tree,test_list,test_reviews)))
	forest_trees_list=[]
	for i in range(forest_trees):
		temptree=tree()
		temptree.treeconstruct(random_list_pos,random_list_neg,forest_index_lists[i])
		forest_trees_list.append(temptree)
	print("forest accuracy : "+str(forest_accuracy(forest_trees_list,test_list,test_reviews)))

	# (random_list_pos,random_list_neg)=addnoice(random_list_pos,random_list_neg,10,review_list)
	# dbfile.close()