import sys
from training import *
from preprocessing import load



if __name__=="__main__":
	if (sys.argv[1] == '2'):
		validation_reviews=load('validationreviews.pkl')
		validation_list=load('validationlist.pkl')
		test_reviews=load('testreviews.pkl')
		test_list=load('testlist.pkl')
		random_list_pos=load('randompos.pkl')
		random_list_neg=load('randomneg.pkl')
		review_list=load('reviewlist.pkl')
		indexlist=load('indexlist.pkl')


		Tree=tree()
		Tree.treeconstruct(random_list_pos,random_list_neg,indexlist,review_list)
		print ("total nodes in decision tree initially : "+str(count_nodes(Tree.root)))
		print ("total leaves in decision tree initially : "+str(count_leaves(Tree.root)))
		h=height(Tree.root)
		print ("height of decision tree initially : "+str(h))
		print ("accuracy on training set : "+str(accuracy(Tree,(random_list_pos+random_list_neg),review_list)))
		print ("accuracy on test set : "+str(accuracy(Tree,test_list,test_reviews)))
		indexcount={}
		count_splitting_times(Tree.root,indexcount)
		count=0
		temp=sorted(indexcount,key=indexcount.get,reverse=True)
		print ("Top 4 splitting indexes:")
		for i in range(1,5):
				print (str(temp[i])+":"+str(indexcount[temp[i]]))
				count=count+1


		EarlyTree=tree()
		EarlyTree.treeconstruct(random_list_pos,random_list_neg,indexlist,review_list,int(h/4))
		print ("total nodes in decision tree for early stopping: "+str(count_nodes(EarlyTree.root)))
		print ("total leaves in decision tree early stopping: "+str(count_leaves(EarlyTree.root)))
		h=height(EarlyTree.root)
		print ("height of decision tree after early stopping : "+str(h))
		print ("accuracy on training set early stopping: "+str(accuracy(EarlyTree,(random_list_pos+random_list_neg),review_list)))
		print ("accuracy on test set early stopping: : "+str(accuracy(EarlyTree,test_list,test_reviews)))
		indexcount={}
		count_splitting_times(EarlyTree.root,indexcount)
		count=0
		temp=sorted(indexcount,key=indexcount.get,reverse=True)
		print ("Top 4 splitting indexes:")
		for i in range(1,5):
				print (str(temp[i])+":"+str(indexcount[temp[i]]))
				count=count+1
		


	elif (sys.argv[1] == '3'):
		validation_reviews=load('validationreviews.pkl')
		validation_list=load('validationlist.pkl')
		test_reviews=load('testreviews.pkl')
		test_list=load('testlist.pkl')
		random_list_pos=load('randompos.pkl')
		random_list_neg=load('randomneg.pkl')
		review_list=load('reviewlist.pkl')
		indexlist=load('indexlist.pkl')

		Tree=tree()
		Tree.treeconstruct(random_list_pos,random_list_neg,indexlist,review_list)
		print ("total nodes in decision tree initially : "+str(count_nodes(Tree.root)))
		print ("total leaves in decision tree initially : "+str(count_leaves(Tree.root)))
		h=height(Tree.root)
		print ("height of decision tree initially : "+str(h))
		print ("accuracy on training set : "+str(accuracy(Tree,(random_list_pos+random_list_neg),review_list)))
		print ("accuracy on test set : "+str(accuracy(Tree,test_list,test_reviews)))

		noice = 5
		(random_list_pos,random_list_neg)=addnoice(random_list_pos,random_list_neg,noice,review_list)
		Tree=tree()
		Tree.treeconstruct(random_list_pos,random_list_neg,indexlist,review_list)
		print ("total nodes in decision tree after noice : "+str(count_nodes(Tree.root)))
		print ("total leaves in decision tree after noice : "+str(count_leaves(Tree.root)))
		h=height(Tree.root)
		print ("height of decision tree after noice : "+str(h))
		print ("accuracy on training set  after noice: "+str(accuracy(Tree,(random_list_pos+random_list_neg),review_list)))
		print ("accuracy on test set  after noice: "+str(accuracy(Tree,test_list,test_reviews)))


	elif (sys.argv[1] == '4'):
		validation_reviews=load('validationreviews.pkl')
		validation_list=load('validationlist.pkl')
		test_reviews=load('testreviews.pkl')
		test_list=load('testlist.pkl')
		random_list_pos=load('randompos.pkl')
		random_list_neg=load('randomneg.pkl')
		review_list=load('reviewlist.pkl')
		indexlist=load('indexlist.pkl')

		Tree=tree()
		Tree.treeconstruct(random_list_pos,random_list_neg,indexlist,review_list)
		print ("total nodes in decision tree initially : "+str(count_nodes(Tree.root)))
		print ("total leaves in decision tree initially : "+str(count_leaves(Tree.root)))
		h=height(Tree.root)
		print ("height of decision tree initially : "+str(h))
		print ("accuracy on training set : "+str(accuracy(Tree,(random_list_pos+random_list_neg),review_list)))
		print ("accuracy on test set : "+str(accuracy(Tree,test_list,test_reviews)))

		pruning(Tree,Tree.root,validation_list,validation_reviews)
		print ("total nodes in training tree after pruning: "+str(count_nodes(Tree.root)))
		print ("total leaves in training tree after pruning : "+str(count_leaves(Tree.root)))
		h=height(Tree.root)
		print ("height of decision tree after pruning : "+str(h))
		print ("accuracy on training set  after pruning: "+str(accuracy(Tree,(random_list_pos+random_list_neg),review_list)))
		print ("accuracy on test set after pruning: "+str(accuracy(Tree,test_list,test_reviews)))

	elif (sys.argv[1] == '5'):
		validation_reviews=load('validationreviews.pkl')
		validation_list=load('validationlist.pkl')
		test_reviews=load('testreviews.pkl')
		test_list=load('testlist.pkl')
		random_list_pos=load('randompos.pkl')
		random_list_neg=load('randomneg.pkl')
		review_list=load('reviewlist.pkl')
		indexlist=load('indexlist.pkl')

		Tree=tree()
		Tree.treeconstruct(random_list_pos,random_list_neg,indexlist,review_list)
		print ("total nodes in decision tree initially : "+str(count_nodes(Tree.root)))
		print ("total leaves in decision tree initially : "+str(count_leaves(Tree.root)))
		h=height(Tree.root)
		print ("height of decision tree initially : "+str(h))
		print ("accuracy on training set : "+str(accuracy(Tree,(random_list_pos+random_list_neg),review_list)))
		print ("accuracy on test set : "+str(accuracy(Tree,test_list,test_reviews)))


		l=[forest_trees]

		for k in l:
			print ("\nNUmber of trees:"+str(k))
			forest_trees=k
			forest_index_lists=[]

			for i in range(forest_trees):
				forest_index_lists.append(random.sample(indexlist,forest_tree_features))
			forest_trees_list=[]
			for i in range(forest_trees):
				temptree=tree()
				temptree.treeconstruct(random_list_pos,random_list_neg,forest_index_lists[i],review_list)
				forest_trees_list.append(temptree)
			print ("forest accuracy on training set : "+str(forest_accuracy(forest_trees_list,(random_list_pos+random_list_neg),review_list)))
			print("forest accuracy on test data: "+str(forest_accuracy(forest_trees_list,test_list,test_reviews)))



